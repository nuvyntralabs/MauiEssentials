#!/usr/bin/env python3
"""Install a MAUI sample APK, tap every clickable button, then uninstall."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time


def adb(serial: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["adb", "-s", serial, *args], capture_output=True, text=True)


def dump_xml(serial: str) -> str:
    adb(serial, "shell", "uiautomator", "dump", "/sdcard/ui.xml")
    adb(serial, "pull", "/sdcard/ui.xml", "/tmp/ui.xml")
    return open("/tmp/ui.xml", encoding="utf-8").read()


def nodes(xml: str) -> list[tuple[str, bool, int, int]]:
    out: list[tuple[str, bool, int, int]] = []
    for match in re.finditer(r"<node[^>]+>", xml):
        node = match.group(0)
        text = re.search(r'text="([^"]*)"', node)
        bounds = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', node)
        clickable = re.search(r'clickable="([^"]+)"', node)
        if not text or not bounds:
            continue
        x1, y1, x2, y2 = map(int, bounds.groups())
        out.append(
            (
                text.group(1).replace("&#10;", " | "),
                clickable.group(1) == "true" if clickable else False,
                (x1 + x2) // 2,
                (y1 + y2) // 2,
            )
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--serial", required=True)
    parser.add_argument("--package", required=True)
    parser.add_argument("--apk", required=True)
    parser.add_argument("--wait", type=float, default=1.6)
    parser.add_argument("--skip", action="append", default=[])
    args = parser.parse_args()

    adb(args.serial, "uninstall", args.package)
    install = adb(args.serial, "install", "--no-incremental", "-r", "-t", args.apk)
    if install.returncode != 0:
        print(install.stdout)
        print(install.stderr, file=sys.stderr)
        return install.returncode

    resolve = adb(
        args.serial,
        "shell",
        "cmd",
        "package",
        "resolve-activity",
        "--brief",
        "-c",
        "android.intent.category.LAUNCHER",
        args.package,
    )
    activity = resolve.stdout.strip().splitlines()[-1]
    print("Activity:", activity)
    start = adb(args.serial, "shell", "am", "start", "-W", "-n", activity)
    print(start.stdout)
    time.sleep(3)
    pid = adb(args.serial, "shell", "pidof", args.package).stdout.strip()
    if not pid:
        print("APP NOT RUNNING", file=sys.stderr)
        return 1

    xml = dump_xml(args.serial)
    buttons: list[tuple[str, int, int]] = []
    for match in re.finditer(r"<node[^>]+>", xml):
        node = match.group(0)
        cls = re.search(r'class="([^"]*)"', node)
        text = re.search(r'text="([^"]*)"', node)
        bounds = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', node)
        clickable = re.search(r'clickable="true"', node)
        if not (cls and text and bounds and clickable):
            continue
        class_name = cls.group(1)
        is_button = "Button" in class_name or class_name.endswith("Button")
        is_field = any(x in class_name for x in ("EditText", "TextInput", "Switch", "CheckBox", "Radio"))
        if is_field:
            continue
        if not is_button:
            # MAUI sometimes wraps a button in a clickable layout.
            label_preview = text.group(1)
            if len(label_preview) > 40 or label_preview.endswith("...") or "@" in label_preview:
                continue
        label = text.group(1).replace("&#10;", " | ")
        if not label:
            continue
        x1, y1, x2, y2 = map(int, bounds.groups())
        buttons.append((label, (x1 + x2) // 2, (y1 + y2) // 2))
    seen: set[str] = set()
    for label, x, y in buttons:
        if label in seen or any(s.lower() in label.lower() for s in args.skip):
            continue
        seen.add(label)
        adb(args.serial, "shell", "input", "tap", str(x), str(y))
        time.sleep(args.wait)
        status = [t for t, _, _, _ in nodes(dump_xml(args.serial)) if t]
        print(f"OK {label!r} -> {status[-1] if status else ''}")

    uninstall = adb(args.serial, "uninstall", args.package)
    print("UNINSTALL", uninstall.stdout.strip() or uninstall.stderr.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
