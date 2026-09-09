#!/usr/bin/env python3
"""Generate 128x128 NuGet icons and wire PackageIcon in every packable plugin."""

from __future__ import annotations

import math
import re
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIZE = 128


def chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def mix(c0: tuple[int, int, int], c1: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return lerp(c0[0], c1[0], t), lerp(c0[1], c1[1], t), lerp(c0[2], c1[2], t)


def dist(x: float, y: float, cx: float, cy: float) -> float:
    return math.hypot(x - cx, y - cy)


def in_circle(x: float, y: float, cx: float, cy: float, r: float) -> bool:
    return dist(x, y, cx, cy) <= r


def in_ring(x: float, y: float, cx: float, cy: float, inner: float, outer: float) -> bool:
    return inner <= dist(x, y, cx, cy) <= outer


def in_rect(x: float, y: float, left: float, top: float, right: float, bottom: float) -> bool:
    return left <= x <= right and top <= y <= bottom


def in_rounded_rect(x: float, y: float, left: float, top: float, right: float, bottom: float, radius: float) -> bool:
    if x < left or x > right or y < top or y > bottom:
        return False
    dx = min(x - left, right - x)
    dy = min(y - top, bottom - y)
    if dx >= radius or dy >= radius:
        return True
    return (dx - radius) ** 2 + (dy - radius) ** 2 <= radius * radius


def seg_dist(x: float, y: float, x1: float, y1: float, x2: float, y2: float) -> float:
    vx, vy = x2 - x1, y2 - y1
    length2 = vx * vx + vy * vy
    if length2 == 0:
        return dist(x, y, x1, y1)
    t = max(0.0, min(1.0, ((x - x1) * vx + (y - y1) * vy) / length2))
    return dist(x, y, x1 + t * vx, y1 + t * vy)


def in_line(x: float, y: float, x1: float, y1: float, x2: float, y2: float, width: float) -> bool:
    return seg_dist(x, y, x1, y1, x2, y2) <= width


def in_triangle(x: float, y: float, a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> bool:
    def sign(p, q, r) -> float:
        return (p[0] - r[0]) * (q[1] - r[1]) - (q[0] - r[0]) * (p[1] - r[1])

    p = (x, y)
    d1, d2, d3 = sign(p, a, b), sign(p, b, c), sign(p, c, a)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)


def in_arc(x: float, y: float, cx: float, cy: float, inner: float, outer: float, start: float, end: float) -> bool:
    if not in_ring(x, y, cx, cy, inner, outer):
        return False
    angle = math.atan2(y - cy, x - cx)
    if angle < 0:
        angle += 2 * math.pi
    start %= 2 * math.pi
    end %= 2 * math.pi
    if start <= end:
        return start <= angle <= end
    return angle >= start or angle <= end


# --- glyphs (return True to paint accent) ------------------------------------

def glyph_pin(x: float, y: float) -> bool:
    if in_circle(x, y, 64, 50, 18):
        return not in_circle(x, y, 64, 50, 7)
    return in_triangle(x, y, (48, 56), (80, 56), (64, 96))


def glyph_wifi(x: float, y: float) -> bool:
    if in_circle(x, y, 64, 86, 5):
        return True
    return (
        in_arc(x, y, 64, 90, 16, 22, math.pi * 1.15, math.pi * 1.85)
        or in_arc(x, y, 64, 90, 28, 34, math.pi * 1.12, math.pi * 1.88)
        or in_arc(x, y, 64, 90, 40, 46, math.pi * 1.10, math.pi * 1.90)
    )


def glyph_pulse(x: float, y: float) -> bool:
    pts = [(30, 66), (42, 66), (50, 40), (58, 90), (66, 54), (74, 66), (98, 66)]
    return any(in_line(x, y, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 3.6) for i in range(len(pts) - 1))


def glyph_clock(x: float, y: float) -> bool:
    if in_ring(x, y, 64, 64, 24, 30):
        return True
    return in_line(x, y, 64, 64, 64, 44, 3.2) or in_line(x, y, 64, 64, 80, 70, 3.2) or in_circle(x, y, 64, 64, 4)


def glyph_queue(x: float, y: float) -> bool:
    bars = ((36, 40, 92, 52), (36, 58, 84, 70), (36, 76, 76, 88))
    return any(in_rounded_rect(x, y, *b, 4) for b in bars)


def glyph_retry(x: float, y: float) -> bool:
    if in_arc(x, y, 64, 66, 20, 27, math.pi * 0.15, math.pi * 1.75):
        return True
    return in_triangle(x, y, (82, 38), (98, 48), (78, 56))


def glyph_upload(x: float, y: float) -> bool:
    if in_rounded_rect(x, y, 40, 78, 88, 94, 5):
        return True
    return (
        in_line(x, y, 64, 38, 64, 76, 4)
        or in_triangle(x, y, (64, 32), (48, 52), (80, 52))
    )


def glyph_device(x: float, y: float) -> bool:
    if in_rounded_rect(x, y, 46, 30, 82, 98, 8):
        return not in_rounded_rect(x, y, 52, 38, 76, 84, 3)
    return False


def glyph_sync(x: float, y: float) -> bool:
    top = in_arc(x, y, 64, 64, 20, 27, math.pi * 1.05, math.pi * 1.95)
    bot = in_arc(x, y, 64, 64, 20, 27, math.pi * 0.05, math.pi * 0.95)
    head_a = in_triangle(x, y, (86, 38), (100, 50), (78, 54))
    head_b = in_triangle(x, y, (42, 90), (28, 78), (50, 74))
    return top or bot or head_a or head_b


def glyph_bell(x: float, y: float) -> bool:
    if in_circle(x, y, 64, 42, 8):
        return True
    if in_rounded_rect(x, y, 44, 44, 84, 80, 16) and y >= 44:
        return True
    return in_rounded_rect(x, y, 40, 76, 88, 86, 4) or in_circle(x, y, 64, 92, 5)


def glyph_shield_check(x: float, y: float) -> bool:
    nx = (x - 64) / 26
    progress = (y - 32) / 68
    if 32 <= y <= 100 and abs(nx) <= 1.0 - progress * 0.55:
        if in_line(x, y, 50, 66, 60, 78, 3.4) or in_line(x, y, 60, 78, 80, 52, 3.4):
            return False
        return True
    return False


def glyph_heart(x: float, y: float) -> bool:
    return (
        in_circle(x, y, 52, 52, 14)
        or in_circle(x, y, 76, 52, 14)
        or in_triangle(x, y, (40, 56), (88, 56), (64, 96))
    )


def glyph_lock(x: float, y: float) -> bool:
    if y <= 58 and in_ring(x, y, 64, 52, 8, 13.5):
        return True
    if in_rounded_rect(x, y, 48, 56, 80, 90, 5):
        return not (in_circle(x, y, 64, 70, 4) or in_rect(x, y, 62, 70, 66, 82))
    return False


def glyph_key(x: float, y: float) -> bool:
    if in_ring(x, y, 46, 64, 8, 14) or in_circle(x, y, 46, 64, 4):
        return True
    if in_rect(x, y, 56, 60, 96, 68):
        return True
    return in_rect(x, y, 84, 68, 90, 80) or in_rect(x, y, 92, 68, 98, 76)


def glyph_circuit(x: float, y: float) -> bool:
    nodes = ((44, 44), (84, 44), (64, 64), (44, 84), (84, 84))
    if any(in_circle(x, y, cx, cy, 6) for cx, cy in nodes):
        return True
    return (
        in_line(x, y, 44, 44, 64, 64, 3)
        or in_line(x, y, 84, 44, 64, 64, 3)
        or in_line(x, y, 64, 64, 44, 84, 3)
        or in_line(x, y, 64, 64, 84, 84, 3)
    )


def glyph_bolt(x: float, y: float) -> bool:
    return in_triangle(x, y, (70, 30), (44, 68), (62, 68)) or in_triangle(x, y, (58, 60), (84, 60), (58, 100))


def glyph_stack(x: float, y: float) -> bool:
    layers = ((40, 40, 88, 54), (40, 58, 88, 72), (40, 76, 88, 90))
    return any(in_rounded_rect(x, y, *box, 5) for box in layers)


def glyph_vault(x: float, y: float) -> bool:
    if in_rounded_rect(x, y, 36, 36, 92, 92, 10):
        if in_ring(x, y, 64, 64, 14, 20) or in_circle(x, y, 64, 64, 6):
            return False
        return not in_circle(x, y, 64, 64, 14)
    return False


def glyph_camera(x: float, y: float) -> bool:
    if in_rounded_rect(x, y, 34, 46, 94, 90, 8):
        return not in_circle(x, y, 64, 68, 12)
    return in_rounded_rect(x, y, 48, 36, 72, 50, 4) or in_circle(x, y, 82, 54, 4)


def glyph_phone(x: float, y: float) -> bool:
    ear = in_rounded_rect(x, y, 36, 30, 80, 52, 11)
    mouth = in_rounded_rect(x, y, 36, 76, 80, 98, 11)
    curve = in_arc(x, y, 50, 64, 20, 30, math.pi * 1.5, math.pi * 0.5)
    return ear or mouth or curve


def glyph_flag(x: float, y: float) -> bool:
    if in_rect(x, y, 40, 32, 46, 98):
        return True
    return in_triangle(x, y, (46, 34), (92, 50), (46, 66))


def glyph_link(x: float, y: float) -> bool:
    a = in_ring(x, y, 52, 64, 11, 17)
    b = in_ring(x, y, 76, 64, 11, 17)
    return a or b


def glyph_gauge(x: float, y: float) -> bool:
    if in_arc(x, y, 64, 78, 24, 31, math.pi, 2 * math.pi):
        return True
    return in_line(x, y, 64, 78, 86, 50, 3.4) or in_circle(x, y, 64, 78, 5)


def glyph_warning(x: float, y: float) -> bool:
    if in_triangle(x, y, (64, 32), (34, 92), (94, 92)):
        return not (in_rect(x, y, 61, 48, 67, 70) or in_circle(x, y, 64, 80, 4))
    return False


def glyph_drop(x: float, y: float) -> bool:
    return in_circle(x, y, 64, 72, 20) or in_triangle(x, y, (64, 32), (46, 68), (82, 68))


def glyph_eye(x: float, y: float) -> bool:
    if in_circle(x, y, 64, 64, 12):
        return not in_circle(x, y, 64, 64, 5)
    return in_arc(x, y, 64, 64, 26, 32, math.pi * 1.15, math.pi * 1.85) or in_arc(
        x, y, 64, 64, 26, 32, math.pi * 0.15, math.pi * 0.85
    )


def glyph_refresh(x: float, y: float) -> bool:
    if in_arc(x, y, 64, 64, 20, 27, math.pi * 0.2, math.pi * 1.7):
        return True
    return in_triangle(x, y, (64, 30), (82, 42), (60, 50))


def glyph_bluetooth(x: float, y: float) -> bool:
    return (
        in_line(x, y, 64, 32, 64, 96, 3.6)
        or in_line(x, y, 64, 32, 86, 50, 3.6)
        or in_line(x, y, 86, 50, 64, 64, 3.6)
        or in_line(x, y, 64, 64, 86, 78, 3.6)
        or in_line(x, y, 86, 78, 64, 96, 3.6)
        or in_line(x, y, 46, 50, 64, 64, 3.6)
        or in_line(x, y, 46, 78, 64, 64, 3.6)
    )


def glyph_clipboard(x: float, y: float) -> bool:
    if in_rounded_rect(x, y, 42, 38, 86, 98, 6):
        return not in_rect(x, y, 50, 56, 78, 62) and not in_rect(x, y, 50, 70, 78, 76) and not in_rect(x, y, 50, 84, 70, 90)
    return in_rounded_rect(x, y, 52, 28, 76, 44, 4)


def glyph_share(x: float, y: float) -> bool:
    nodes = ((44, 64), (84, 42), (84, 86))
    if any(in_circle(x, y, cx, cy, 7) for cx, cy in nodes):
        return True
    return in_line(x, y, 44, 64, 84, 42, 3.2) or in_line(x, y, 44, 64, 84, 86, 3.2)


def glyph_chip(x: float, y: float) -> bool:
    if in_rounded_rect(x, y, 44, 44, 84, 84, 6):
        return not in_rounded_rect(x, y, 54, 54, 74, 74, 3)
    pins = []
    for i in range(3):
        pins.append(in_rect(x, y, 50 + i * 10, 34, 56 + i * 10, 44))
        pins.append(in_rect(x, y, 50 + i * 10, 84, 56 + i * 10, 94))
        pins.append(in_rect(x, y, 34, 50 + i * 10, 44, 56 + i * 10))
        pins.append(in_rect(x, y, 84, 50 + i * 10, 94, 56 + i * 10))
    return any(pins)


def glyph_nfc(x: float, y: float) -> bool:
    return (
        in_arc(x, y, 48, 64, 10, 16, math.pi * 1.55, math.pi * 0.45)
        or in_arc(x, y, 48, 64, 22, 28, math.pi * 1.55, math.pi * 0.45)
        or in_arc(x, y, 48, 64, 34, 40, math.pi * 1.55, math.pi * 0.45)
        or in_circle(x, y, 48, 64, 5)
    )


def glyph_app_lock(x: float, y: float) -> bool:
    if y <= 50 and in_ring(x, y, 64, 46, 7, 12):
        return True
    if in_rounded_rect(x, y, 50, 50, 78, 78, 4):
        return not in_circle(x, y, 64, 62, 3.2)
    return in_ring(x, y, 64, 90, 6, 10) or in_line(x, y, 64, 90, 70, 84, 2.4)


def glyph_check(x: float, y: float) -> bool:
    if in_rounded_rect(x, y, 36, 36, 92, 92, 10):
        return not (in_line(x, y, 48, 66, 60, 80, 4) or in_line(x, y, 60, 80, 84, 50, 4))
    return False


def glyph_printer(x: float, y: float) -> bool:
    if in_rounded_rect(x, y, 34, 52, 94, 86, 6):
        return not in_rect(x, y, 78, 62, 88, 70)
    return in_rounded_rect(x, y, 46, 32, 82, 54, 3) or in_rounded_rect(x, y, 46, 80, 82, 100, 3)


def glyph_keyboard(x: float, y: float) -> bool:
    if not in_rounded_rect(x, y, 30, 46, 98, 86, 8):
        return False
    for row, count, x0 in ((54, 7, 38), (66, 7, 38), (78, 5, 46)):
        for i in range(count):
            if in_rounded_rect(x, y, x0 + i * 8, row - 3, x0 + i * 8 + 6, row + 3, 1.2):
                return False
    return True


def glyph_rotate(x: float, y: float) -> bool:
    phone = in_rounded_rect(x, y, 50, 40, 78, 88, 6) and not in_rounded_rect(x, y, 55, 46, 73, 78, 2)
    arrow = in_arc(x, y, 64, 64, 34, 40, math.pi * 1.2, math.pi * 1.9) or in_triangle(x, y, (40, 34), (54, 28), (50, 46))
    return phone or arrow


def glyph_toolkit(x: float, y: float) -> bool:
    ring = in_circle(x, y, 64, 64, 26) and not in_circle(x, y, 64, 64, 16)
    plus = in_rect(x, y, 60, 48, 68, 80) or in_rect(x, y, 48, 60, 80, 68)
    return ring or plus


def glyph_layers(x: float, y: float) -> bool:
    boxes = ((40, 36, 80, 68), (44, 48, 84, 80), (48, 60, 88, 92))
    hits = [in_rounded_rect(x, y, *box, 6) for box in boxes]
    return any(hits)


def glyph_window(x: float, y: float) -> bool:
    outer = in_rounded_rect(x, y, 34, 36, 94, 94, 8)
    inner = in_rounded_rect(x, y, 40, 54, 88, 88, 3)
    if not (outer and not inner):
        return False
    return not (in_circle(x, y, 44, 44, 3.2) or in_circle(x, y, 54, 44, 3.2))


Theme = tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]

THEMES: dict[str, Theme] = {
    "teal": ((15, 40, 70), (20, 140, 150), (16, 122, 128), (236, 248, 247)),
    "green": ((14, 42, 32), (22, 130, 80), (15, 118, 70), (236, 250, 242)),
    "blue": ((16, 32, 72), (30, 90, 170), (20, 80, 160), (236, 244, 252)),
    "indigo": ((24, 24, 64), (70, 60, 170), (67, 56, 150), (240, 238, 252)),
    "slate": ((15, 23, 42), (50, 70, 100), (30, 50, 80), (241, 245, 249)),
    "amber": ((50, 30, 10), (180, 120, 30), (180, 110, 20), (255, 248, 235)),
    "orange": ((50, 24, 10), (200, 90, 30), (194, 80, 20), (255, 244, 236)),
    "rose": ((50, 16, 32), (180, 50, 90), (170, 40, 80), (255, 241, 246)),
    "purple": ((36, 16, 56), (120, 50, 160), (110, 40, 150), (246, 240, 252)),
    "cyan": ((10, 40, 56), (20, 140, 160), (14, 116, 144), (236, 254, 255)),
    "navy": ((10, 20, 48), (20, 50, 110), (15, 40, 90), (236, 242, 250)),
}

ICONS: dict[str, tuple[str, object]] = {
    "ApiCache": ("slate", glyph_stack),
    "ApiResilience": ("blue", glyph_circuit),
    "AppHealth": ("green", glyph_heart),
    "AppLock": ("navy", glyph_app_lock),
    "AppUpdate": ("green", glyph_refresh),
    "BackgroundTasks": ("indigo", glyph_clock),
    "BluetoothManager": ("blue", glyph_bluetooth),
    "ClipboardPlus": ("slate", glyph_clipboard),
    "CommunityToolkitPlus": ("purple", glyph_toolkit),
    "DeepLinks": ("blue", glyph_link),
    "DeviceInfoPlus": ("purple", glyph_chip),
    "DeviceOrientation": ("teal", glyph_rotate),
    "DeviceSession": ("purple", glyph_device),
    "Diagnostics": ("rose", glyph_warning),
    "FeatureFlags": ("orange", glyph_flag),
    "FileVault": ("amber", glyph_vault),
    "FormValidation": ("green", glyph_check),
    "GeoLocator": ("green", glyph_pin),
    "HttpForge": ("indigo", glyph_bolt),
    "JobQueue": ("blue", glyph_queue),
    "KeyboardManager": ("indigo", glyph_keyboard),
    "LeakAnalyser": ("cyan", glyph_drop),
    "MVVMExpress": ("indigo", glyph_layers),
    "MediaPipeline": ("rose", glyph_camera),
    "NetworkDiagnostics": ("amber", glyph_pulse),
    "NetworkMonitor": ("slate", glyph_wifi),
    "Nfc": ("amber", glyph_nfc),
    "Observability": ("indigo", glyph_eye),
    "OfflineSync": ("teal", glyph_sync),
    "Performance": ("purple", glyph_gauge),
    "PermissionFlow": ("amber", glyph_shield_check),
    "Printing": ("slate", glyph_printer),
    "PushRouter": ("rose", glyph_bell),
    "RetryQueue": ("orange", glyph_retry),
    "SecureSession": ("teal", glyph_key),
    "SecureStoragePlus": ("teal", glyph_lock),
    "SharePlus": ("teal", glyph_share),
    "SmartUpload": ("cyan", glyph_upload),
    "VoipCore": ("green", glyph_phone),
    "WpfMVVMExpress": ("navy", glyph_window),
    "WinUIMVVMExpress": ("indigo", glyph_window),
    "AvaloniaMVVMExpress": ("purple", glyph_layers),
    "UnoMVVMExpress": ("cyan", glyph_layers),
}


def in_card(x: int, y: int, size: int) -> bool:
    margin = 14
    radius = 12
    return in_rounded_rect(x, y, margin, margin, size - margin - 1, size - margin - 1, radius)


def pixel(x: int, y: int, size: int, theme: Theme, glyph) -> bytes:
    bg0, bg1, accent, card = theme
    t = (x + y) / (2 * (size - 1))
    r, g, b = mix(bg0, bg1, t)
    if in_card(x, y, size):
        r, g, b = card
        if glyph(x, y):
            r, g, b = accent
    return bytes((r, g, b, 255))


def write_png(path: Path, theme: Theme, glyph, size: int = SIZE) -> None:
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        for x in range(size):
            raw.extend(pixel(x, y, size, theme, glyph))
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def generate_icons() -> list[Path]:
    written: list[Path] = []
    for plugin, (theme_name, glyph) in ICONS.items():
        dest = ROOT / plugin / "nuget.png"
        dest.parent.mkdir(parents=True, exist_ok=True)
        write_png(dest, THEMES[theme_name], glyph)
        written.append(dest)
    return written


ICON_PROPERTY = "<PackageIcon>icon.png</PackageIcon>"
ICON_ITEM = '<None Include="..\\..\\nuget.png" Pack="true" PackagePath="icon.png" />'


def _indent_of(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" \t"))]


def patch_csproj(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "<PackageId>" not in text:
        return False
    packable = re.search(r"<IsPackable>(.*?)</IsPackable>", text)
    if packable and packable.group(1).strip().lower() == "false":
        return False

    changed = False
    if "<PackageIcon>" not in text:
        readme = re.search(r"^([ \t]*)<PackageReadmeFile>.*</PackageReadmeFile>\s*$", text, re.M)
        if readme:
            text = text.replace(readme.group(0), f"{readme.group(0)}\n{readme.group(1)}{ICON_PROPERTY}", 1)
        else:
            pkg = re.search(r"^([ \t]*)<PackageId>.*</PackageId>\s*$", text, re.M)
            if not pkg:
                return False
            text = text.replace(pkg.group(0), f"{pkg.group(0)}\n{pkg.group(1)}{ICON_PROPERTY}", 1)
        changed = True

    if "nuget.png" not in text:
        license_line = None
        for line in text.splitlines():
            if "LICENSE" in line and "Pack=" in line and "<None" in line:
                license_line = line
        if license_line:
            text = text.replace(license_line, f"{license_line}\n{_indent_of(license_line)}{ICON_ITEM}", 1)
        else:
            text = text.replace("</Project>", f"  <ItemGroup>\n    {ICON_ITEM}\n  </ItemGroup>\n</Project>", 1)
        changed = True

    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def patch_projects() -> list[Path]:
    patched: list[Path] = []
    for csproj in sorted(ROOT.glob("*/src/**/*.csproj")):
        if patch_csproj(csproj):
            patched.append(csproj)
    return patched


if __name__ == "__main__":
    icons = generate_icons()
    projects = patch_projects()
    print(f"Wrote {len(icons)} nuget.png files")
    print(f"Updated {len(projects)} packable csproj files")
