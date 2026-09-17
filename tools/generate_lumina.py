#!/usr/bin/env python3
"""Generate the NuvyntraLabs.Lumina submodule: Core + 5 standalone MAUI apps."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path("/Users/niladri/Microsoft/Personal/MauiEssentials")
OUT = ROOT / "Lumina"
TEMPLATE = ROOT / "MVVMExpress/templates/maui-app/MauiApp1"
UIKIT_SAMPLE = ROOT / "UIKit/samples/NuvyntraLabs.UIKit.Sample"

APPS = [
    {
        "id": "Market",
        "title": "Lumina Market",
        "tagline": "Retail, grocery, and food — warm paper, aurora accent.",
        "accent": "#1FA87A",
        "app_id": "com.nuvyntralabs.lumina.market",
        "start": "Walkthrough",
        "home": "Home",
        "letter": "M",
        "screens": [
            ("Walkthrough", "auth", "Three beats before the store opens.",
             [("Welcome to Market", "Groceries, plates, and pantry in one aisle."),
              ("Same-day slots", " couriers from Harbour Studio."),
              ("Pay once", "Cards, wallet, or kitchen tab.")],
             ["SignIn"]),
            ("SignIn", "auth", "Staff and members use the same gate.",
             [("Email", "demo@lumina.market"), ("Password", "secret")],
             ["Home", "SignUp", "ForgotPassword"]),
            ("SignUp", "form", "Create a Market account.",
             [("Full name", "Ada Lovelace"), ("Email", "ada@lumina.market"), ("Phone", "+44 20 7946 0018")],
             ["SignIn", "ProfileSetup"]),
            ("ForgotPassword", "form", "Send a reset link to the inbox.",
             [("Email", "demo@lumina.market")],
             ["ResetPassword", "SignIn"]),
            ("ResetPassword", "form", "OTP then a new secret.",
             [("OTP", "184392"), ("New password", "••••••••")],
             ["SignIn"]),
            ("ProfileSetup", "form", "Avatar, kitchen name, delivery default.",
             [("Display name", "Ada"), ("Kitchen", "Studio loft")],
             ["Home"]),
            ("Home", "home", "Today at Harbour Market.",
             [("Aurora pears", "£3.40 · orchard crate"),
              ("Cedar chair", "£186 · weekend drop"),
              ("Harbour ramen", "£14 · 22 min")],
             ["Categories", "Catalog", "Search", "Cart", "Orders", "Notifications", "Settings"]),
            ("Categories", "list", "Aisles you actually walk.",
             [("Produce", "84 items"), ("Home", "61 items"), ("Kitchen", "47 items"), ("Ready to eat", "29 items")],
             ["Catalog", "Search"]),
            ("Catalog", "list", "Tile grid of this week's drop.",
             [("Aurora lamp", "£42"), ("Harbour mug", "£18"), ("Linen throw", "£64"), ("Cedar chair", "£186")],
             ["ProductDetail", "Filters", "Compare"]),
            ("ProductDetail", "detail", "Cedar lounge chair — oiled oak, wool seat.",
             [("Finish", "White oak"), ("Lead time", "5 days"), ("Rating", "4.8 · 216 reviews")],
             ["Cart", "Wishlist", "Reviews", "Compare"]),
            ("Compare", "list", "Chair vs chair.",
             [("Cedar lounge", "£186 · wool"), ("Studio stool", "£92 · leather")],
             ["ProductDetail", "Cart"]),
            ("Search", "list", "Type a room or a craving.",
             [("pears", "12 matches"), ("oak chair", "4 matches"), ("ramen", "6 matches")],
             ["Filters", "ProductDetail"]),
            ("Filters", "form", "Price, aisle, and delivery window.",
             [("Max price", "£80"), ("Aisle", "Home"), ("Window", "Today 4–6")],
             ["Catalog"]),
            ("Wishlist", "list", "Saved for later.",
             [("Linen throw", "£64"), ("Harbour mug", "£18")],
             ["ProductDetail", "Cart"]),
            ("Cart", "list", "Two lines, one kitchen.",
             [("Aurora pears × 2", "£6.80"), ("Harbour ramen × 1", "£14.00")],
             ["Checkout", "Wishlist"]),
            ("Checkout", "form", "Address plus slot.",
             [("Address", "14 Harbour Walk"), ("Slot", "Today 17:30"), ("Note", "Leave at studio door")],
             ["CardPayment", "Addresses"]),
            ("CardPayment", "form", "Masked PAN on warm paper.",
             [("Card", "4242 4242 4242 4242"), ("Expiry", "09 / 28"), ("CVC", "317")],
             ["PaymentResult", "SavedCards"]),
            ("SavedCards", "list", "Instruments on file.",
             [("Visa ··4242", "Ada Lovelace"), ("Kitchen tab", "Harbour Studio")],
             ["CardPayment"]),
            ("PaymentResult", "detail", "Paid. Courier is packing.",
             [("Order", "#LM-1042"), ("Total", "£20.80"), ("ETA", "17:52")],
             ["Tracking", "Orders", "Receipt"]),
            ("Orders", "list", "Open tickets.",
             [("#LM-1042", "Packing · £20.80"), ("#LM-1008", "Delivered · £64.00")],
             ["OrderDetail", "Tracking"]),
            ("OrderDetail", "detail", "Harbour ramen + pears.",
             [("Placed", "Today 16:04"), ("Courier", "Nia Okonkwo"), ("Total", "£20.80")],
             ["Tracking", "Invoice", "Receipt", "SellerChat"]),
            ("Tracking", "detail", "Packed → ship → door.",
             [("Packed", "16:11"), ("Ship", "16:40"), ("Door", "17:52")],
             ["OrderDetail", "SellerChat"]),
            ("Invoice", "detail", "Studio invoice LM-1042.",
             [("Produce", "£6.80"), ("Kitchen", "£14.00"), ("Total", "£20.80")],
             ["Receipt", "Orders"]),
            ("Receipt", "detail", "Thermal-style ticket.",
             [("Merchant", "Lumina Market"), ("Auth", "184392"), ("Total", "£20.80")],
             ["Orders"]),
            ("Reviews", "form", "Stars plus a short note.",
             [("Rating", "5"), ("Note", "The oak smells like the workshop.")],
             ["ProductDetail"]),
            ("StoreLocator", "list", "Studios that still have stock.",
             [("Harbour Walk", "0.4 mi · open"), ("Cedar Yard", "1.8 mi · closes 20:00")],
             ["Catalog"]),
            ("Addresses", "list", "Where crates land.",
             [("Studio loft", "14 Harbour Walk"), ("Office", "2 Aurora Lane")],
             ["Checkout"]),
            ("Subscription", "detail", "Weekly produce crate.",
             [("Plan", "Aurora crate"), ("Price", "£28 / week"), ("Next", "Thursday")],
             ["Checkout", "Settings"]),
            ("SellerChat", "chat", "Thread with Harbour Kitchen.",
             [("You", "Can the ramen skip chilli?"), ("Kitchen", "Done. 22 minutes.")],
             ["OrderDetail"]),
            ("Notifications", "list", "Pushes you would have felt.",
             [("Courier nearby", "Nia is 4 minutes out"), ("Crate packed", "Thursday aurora crate")],
             ["Orders", "Tracking"]),
            ("Settings", "form", "Theme, flags, lock.",
             [("Dark paper", "Off"), ("New checkout", "On"), ("Review prompt", "Later")],
             ["Help", "Subscription", "StoreLocator"]),
            ("Help", "list", "How Market works.",
             [("Slots", "Same-day until 19:00"), ("Returns", "7 days on home goods")],
             ["Settings"]),
        ],
    },
    {
        "id": "Clinic",
        "title": "Nuvexa Clinic",
        "tagline": "Appointments, pharmacy, labs, and a quiet in-call room.",
        "accent": "#2F7DE1",
        "app_id": "com.nuvyntralabs.lumina.clinic",
        "start": "Walkthrough",
        "home": "Home",
        "letter": "C",
        "screens": [
            ("Walkthrough", "auth", "Care without the clipboard pile.",
             [("Find a clinician", "Same-week slots."),
              ("Bring records", "Labs and letters in one file."),
              ("Call when needed", "In-app visit room.")],
             ["SignIn"]),
            ("SignIn", "auth", "Patients and clinicians.",
             [("Email", "demo@nuvexa.clinic"), ("Password", "secret")],
             ["Home", "HealthProfile"]),
            ("HealthProfile", "detail", "Ada Lovelace · 36 · London.",
             [("Blood type", "O+"), ("Allergies", "Penicillin"), ("GP", "Dr. Iyer")],
             ["Home", "Vitals"]),
            ("Home", "home", "Today at Nuvexa Clinic.",
             [("09:30", "Dr. Iyer · follow-up"),
              ("Lab", "Lipid panel ready"),
              ("Rx", "Atorvastatin 10 mg")],
             ["Appointments", "Doctors", "Pharmacy", "LabResults", "Inbox", "Notifications", "Settings"]),
            ("Appointments", "list", "Upcoming and past.",
             [("Thu 09:30", "Cardiology · Dr. Iyer"), ("Mon 14:00", "Physio · Lin Park")],
             ["Booking", "VisitDetail"]),
            ("Booking", "form", "Pick a slot on the calendar.",
             [("Clinic", "Harbour"), ("Reason", "Follow-up"), ("Slot", "Thu 09:30")],
             ["Appointments", "Doctors"]),
            ("Doctors", "list", "Directory.",
             [("Dr. Priya Iyer", "Cardiology · 4.9"), ("Lin Park", "Physio · 4.8"), ("Noah Adeyemi", "GP · 4.7")],
             ["DoctorProfile", "Booking"]),
            ("DoctorProfile", "detail", "Dr. Priya Iyer — cardiology.",
             [("Languages", "EN, HI"), ("Next slot", "Thu 09:30"), ("Clinic", "Harbour 3F")],
             ["Booking", "Inbox"]),
            ("VisitDetail", "detail", "Follow-up after lipid panel.",
             [("Notes", "Continue statin. Walk 30 min."), ("BP", "118 / 74"), ("Next", "12 weeks")],
             ["Prescriptions", "Documents", "Invoice"]),
            ("Prescriptions", "list", "Active scripts.",
             [("Atorvastatin 10 mg", "Nightly · 28 days"), ("Vitamin D3", "Weekly")],
             ["Pharmacy", "VisitDetail"]),
            ("Pharmacy", "list", "Harbour pharmacy counter.",
             [("Atorvastatin", "£6.40 · ready"), ("D3 2000 IU", "£4.10")],
             ["PharmacyDetail", "Prescriptions"]),
            ("PharmacyDetail", "detail", "Atorvastatin 10 mg film-coated.",
             [("Stock", "Ready in 20 min"), ("Interactions", "Grapefruit"), ("Price", "£6.40")],
             ["Pharmacy"]),
            ("LabResults", "list", "Panels in the last year.",
             [("Lipids", "Ready · 12 Sep"), ("CBC", "Ready · 2 Jun"), ("HbA1c", "Ready · 2 Jun")],
             ["LabDetail"]),
            ("LabDetail", "detail", "Lipid panel — 12 Sep 2026.",
             [("LDL", "2.1 mmol/L"), ("HDL", "1.6 mmol/L"), ("Trig", "1.1 mmol/L")],
             ["VisitDetail", "Documents"]),
            ("Documents", "list", "Letters and PDFs.",
             [("Discharge", "Brief.pdf"), ("Referral", "Physio letter")],
             ["VisitDetail"]),
            ("Invoice", "detail", "Visit 12 Sep.",
             [("Consult", "£85"), ("ECG", "£40"), ("Total", "£125")],
             ["VisitDetail"]),
            ("Inbox", "list", "Care threads.",
             [("Dr. Iyer", "Your lipids look better."), ("Pharmacy", "Script is ready.")],
             ["Conversation", "InCall"]),
            ("Conversation", "chat", "Thread with Dr. Iyer.",
             [("Iyer", "Continue the statin."), ("You", "Walking most evenings.")],
             ["Inbox", "InCall"]),
            ("InCall", "detail", "Video room — on hold chrome.",
             [("Peer", "Dr. Iyer"), ("Quality", "Good"), ("Duration", "00:12:04")],
             ["Conversation"]),
            ("Insurance", "detail", "Nuvexa Care · member 8841.",
             [("Plan", "Harbour Plus"), ("Excess", "£150"), ("Valid", "2027-03")],
             ["Settings"]),
            ("Departments", "list", "Floors in the Harbour building.",
             [("Cardiology", "3F"), ("Imaging", "B1"), ("Pharmacy", "G")],
             ["Doctors"]),
            ("Vitals", "detail", "Home readings this week.",
             [("HR", "72"), ("BP", "118 / 74"), ("Weight", "64.2 kg")],
             ["HealthProfile"]),
            ("Medications", "list", "Today's box.",
             [("21:00", "Atorvastatin"), ("Sunday", "D3")],
             ["Prescriptions"]),
            ("Faq", "list", "Clinic questions.",
             [("Late?", "Call the desk before 15 min."), ("Records", "PDF in Documents.")],
             ["Help"]),
            ("Help", "list", "Desk and after-hours.",
             [("Desk", "020 7946 1000"), ("After hours", "On-call GP")],
             ["Faq", "Settings"]),
            ("Notifications", "list", "Reminders.",
             [("Thu 09:30", "Bring your wearable."), ("Rx ready", "Harbour pharmacy")],
             ["Appointments"]),
            ("Settings", "form", "Privacy and flags.",
             [("Share labs", "On"), ("Telehealth", "On")],
             ["Insurance", "HealthProfile", "Help"]),
        ],
    },
    {
        "id": "Field",
        "title": "Harbor Field",
        "tagline": "Jobs, inspections, NFC assets, and an offline queue.",
        "accent": "#C4841D",
        "app_id": "com.nuvyntralabs.lumina.field",
        "start": "SignIn",
        "home": "Home",
        "letter": "F",
        "screens": [
            ("SignIn", "auth", "Crew gate. PIN on the van tablet.",
             [("Crew id", "HF-441"), ("Password", "secret")],
             ["Home"]),
            ("Home", "home", "Harbour district — Tuesday board.",
             [("HF-204", "Inspect pump · Cedar Yard"),
              ("HF-188", "NFC audit · Pier 3"),
              ("Queue", "2 photos waiting")],
             ["Jobs", "Sites", "Assets", "OfflineQueue", "Dashboard", "Notifications", "Settings"]),
            ("Jobs", "list", "Assigned work.",
             [("HF-204", "Inspect · 09:30"), ("HF-188", "NFC · 11:00"), ("HF-175", "Print · 14:00")],
             ["JobDetail", "Route"]),
            ("JobDetail", "detail", "HF-204 — storm pump, Cedar Yard.",
             [("SLA", "Today 16:00"), ("Site", "Yard B"), ("Parts", "Gasket kit")],
             ["Inspection", "Evidence", "Sites", "Team"]),
            ("Sites", "list", "Yards on the fence list.",
             [("Cedar Yard", "Geofence in"), ("Pier 3", "0.8 mi"), ("Harbour Walk", "1.4 mi")],
             ["Geofences", "JobDetail"]),
            ("Geofences", "list", "Twenty circles max.",
             [("Cedar Yard", "80 m · dwell 5 min"), ("Pier 3", "50 m · enter")],
             ["Sites", "Route"]),
            ("Inspection", "form", "Checklist on the pump.",
             [("Housing", "OK"), ("Gasket", "Replace"), ("Tag", "NFC written")],
             ["Evidence", "JobDetail", "Checklist"]),
            ("Evidence", "list", "Photos queued for upload.",
             [("housing.jpg", "1.8 MB · ready"), ("gasket.jpg", "2.1 MB · queued")],
             ["Inspection", "OfflineQueue"]),
            ("NfcScan", "detail", "Hold the puck to the asset plate.",
             [("Tag", "04:A3:19:88"), ("Asset", "PUMP-441"), ("Last", "12 Sep")],
             ["Assets", "AssetDetail"]),
            ("Assets", "list", "Yard register.",
             [("PUMP-441", "Cedar · OK"), ("GEN-12", "Pier 3 · due"), ("RADIO-9", "Van · OK")],
             ["AssetDetail", "NfcScan"]),
            ("AssetDetail", "detail", "PUMP-441 — Flygt storm pump.",
             [("Hours", "1 842"), ("Next service", "Oct 2026"), ("NFC", "04:A3:19:88")],
             ["Inspection", "Files"]),
            ("Conflicts", "detail", "Offline write vs desk edit.",
             [("Local", "Gasket replace"), ("Desk", "Gasket OK"), ("Pick", "Local")],
             ["OfflineQueue", "JobDetail"]),
            ("OfflineQueue", "list", "Waiting for real internet.",
             [("photo gasket", "Retry 30s"), ("NFC write", "Retry 2 min")],
             ["Conflicts", "Evidence"]),
            ("Printers", "list", "SPP and BLE receipts.",
             [("Zebra ZQ", "SPP · paired"), ("Harbour desk", "BLE · idle")],
             ["Receipt"]),
            ("Receipt", "detail", "Job ticket HF-204.",
             [("Work", "Gasket replace"), ("Hours", "1.2"), ("Sign", "Nia")],
             ["Printers", "JobDetail"]),
            ("Timesheet", "list", "Tuesday hours.",
             [("HF-204", "1.2 h"), ("HF-188", "0.8 h"), ("Travel", "0.4 h")],
             ["Dashboard", "Jobs"]),
            ("Dashboard", "home", "Crew week.",
             [("Open", "3"), ("Overdue", "0"), ("Queue", "2")],
             ["Jobs", "Timesheet"]),
            ("Files", "list", "Drawings on the device.",
             [("pump-441.pdf", "2 pages"), ("yard-b.png", "site plan")],
             ["AssetDetail"]),
            ("Checklist", "form", "Safety before the hatch.",
             [("PPE", "On"), ("Lockout", "On"), ("Spotter", "Nia")],
             ["Safety", "Inspection"]),
            ("Safety", "detail", "Brief — confined space.",
             [("Permit", "CS-19"), ("Gas", "Clear 08:50"), ("Radio", "Ch 4")],
             ["Checklist", "JobDetail"]),
            ("Route", "detail", "Van plan.",
             [("1", "Cedar Yard"), ("2", "Pier 3"), ("3", "Desk print")],
             ["Jobs", "Geofences"]),
            ("Team", "chat", "Crew 4 thread.",
             [("Nia", "Gasket kit is in the van."), ("You", "On site in 10.")],
             ["JobDetail"]),
            ("Notifications", "list", "Dispatch.",
             [("HF-204", "SLA in 4 hours"), ("Fence", "Entered Cedar Yard")],
             ["Jobs"]),
            ("Settings", "form", "Keep-awake, offline, pins.",
             [("Keep screen on", "On"), ("Offline first", "On")],
             ["Dashboard", "Printers"]),
        ],
    },
    {
        "id": "Bank",
        "title": "Aether Bank",
        "tagline": "Accounts, cards, wealth, and a lock that actually locks.",
        "accent": "#3D4A8F",
        "app_id": "com.nuvyntralabs.lumina.bank",
        "start": "SignIn",
        "home": "Dashboard",
        "letter": "A",
        "screens": [
            ("SignIn", "auth", "Member number or email.",
             [("Email", "demo@aether.bank"), ("Password", "secret")],
             ["PinLock"]),
            ("PinLock", "auth", "Six digits after background.",
             [("PIN", "••••18")],
             ["Dashboard"]),
            ("Dashboard", "home", "Good afternoon, Ada.",
             [("Current", "£4,812.20"), ("Savings", "£18,440.00"), ("Cards", "Spend £220 this week")],
             ["Accounts", "Cards", "Transfer", "Invest", "Notifications", "Settings"]),
            ("Accounts", "list", "Sterling books.",
             [("Current · 8841", "£4,812.20"), ("Savings · 2290", "£18,440.00"), ("USD travel", "$1,240.00")],
             ["AccountDetail", "Statements"]),
            ("AccountDetail", "detail", "Current 40-88-41.",
             [("Available", "£4,812.20"), ("Pending", "£42.00"), ("IBAN", "GB82 AETH 4044 8841")],
             ["Transfer", "Statements", "Invoice"]),
            ("Cards", "list", "Plastic and metal.",
             [("Debit aurora", "··4418"), ("Metal travel", "··2290 · locked")],
             ["CardDetail"]),
            ("CardDetail", "detail", "Aurora debit ··4418.",
             [("Limit", "£1,500"), ("Contactless", "On"), ("Frozen", "Off")],
             ["Cards", "AppLock"]),
            ("Transfer", "form", "Pay a person or a bill.",
             [("To", "Lin Park"), ("Amount", "£85.00"), ("Ref", "Dinner")],
             ["Payees", "Bills"]),
            ("Payees", "list", "Trusted names.",
             [("Lin Park", "40-12-88 · 22901122"), ("Harbour Market", "sort 20-00-00")],
             ["Transfer", "Beneficiaries"]),
            ("Bills", "list", "Due this month.",
             [("Council", "£142 · 20 Sep"), ("Thames", "£38 · 22 Sep")],
             ["BillDetail", "Transfer"]),
            ("BillDetail", "detail", "Council tax — September.",
             [("Due", "20 Sep"), ("Amount", "£142"), ("Account", "Current")],
             ["Bills", "Transfer"]),
            ("Invest", "list", "Wealth sleeves.",
             [("Aurora 80", "+1.4% YTD"), ("Cash plus", "+0.6%")],
             ["InvestDetail"]),
            ("InvestDetail", "detail", "Aurora 80 — global equity tilt.",
             [("Value", "£9,220"), ("ISIN", "IE00B4L5Y983"), ("Risk", "5 / 7")],
             ["Invest", "Statements"]),
            ("Kyc", "form", "Refresh your file.",
             [("Address", "14 Harbour Walk"), ("Occupation", "Engineer"), ("Source", "Salary")],
             ["Settings"]),
            ("Statements", "list", "PDF months.",
             [("Aug 2026", "Current.pdf"), ("Jul 2026", "Current.pdf")],
             ["AccountDetail", "Invoice"]),
            ("Invoice", "detail", "Advice note 12 Sep.",
             [("FX", "$200 → £156.40"), ("Fee", "£0.00")],
             ["AccountDetail"]),
            ("Loans", "list", "Open credit.",
             [("Studio loan", "£12,400 left"), ("Overdraft", "£250 unused")],
             ["LoanDetail"]),
            ("LoanDetail", "detail", "Studio loan — 4.2% APR.",
             [("Next", "£220 on 1 Oct"), ("End", "2029-04")],
             ["Loans", "Transfer"]),
            ("Rewards", "detail", "Aurora points.",
             [("Balance", "8 420"), ("Rate", "1% debit"), ("Next", "Market crate")],
             ["Cards"]),
            ("Beneficiaries", "list", "International.",
             [("Padhy Studio", "IN · HDFC"), ("Lina Chen", "SG · DBS")],
             ["Payees", "Transfer"]),
            ("Support", "chat", "Secure inbox.",
             [("Aether", "We froze the travel card."), ("You", "Thank you — unlock Friday.")],
             ["CardDetail"]),
            ("Notifications", "list", "Money moving.",
             [("£85 to Lin", "Just now"), ("Card tap", "Harbour Market £14")],
             ["Accounts", "Cards"]),
            ("AppLock", "form", "Timer, Face ID, screenshot guard.",
             [("Lock after", "30 s"), ("Biometric", "On"), ("Screen guard", "On")],
             ["PinLock", "Settings"]),
            ("Settings", "form", "Limits and flags.",
             [("Travel mode", "Off"), ("Wealth", "On")],
             ["Kyc", "AppLock", "Support"]),
        ],
    },
    {
        "id": "Civic",
        "title": "Civic Pulse",
        "tagline": "City services, transit, events, and a civic wallet.",
        "accent": "#C23B2E",
        "app_id": "com.nuvyntralabs.lumina.civic",
        "start": "SignIn",
        "home": "Home",
        "letter": "P",
        "screens": [
            ("SignIn", "auth", "Resident pass.",
             [("Email", "demo@civic.pulse"), ("Password", "secret")],
             ["Home"]),
            ("Home", "home", "Harbour borough today.",
             [("Bin day", "Thursday · food + recycling"),
              ("Bus 12", "4 min · Harbour Walk"),
              ("Market", "Night market 18:00")],
             ["Services", "Transit", "Events", "News", "Wallet", "Notifications", "Settings"]),
            ("Services", "list", "Requests the desk still owns.",
             [("Missed bin", "Open · 2 days"), ("Pothole", "Scheduled"), ("Permit", "Ready")],
             ["RequestDetail", "Permits"]),
            ("RequestDetail", "detail", "Missed food-waste bin.",
             [("Ref", "CR-4418"), ("Crew", "Thursday am"), ("Photo", "Attached")],
             ["Services", "Offices"]),
            ("Transit", "list", "Live-looking times, static clock.",
             [("Bus 12", "4 min"), ("Ferry", "18 min"), ("Night", "00:20")],
             ["TicketDetail", "Booking"]),
            ("TicketDetail", "detail", "Day rover — QR on paper.",
             [("Zones", "1–2"), ("Valid", "Until 04:00"), ("Fare", "£8.40")],
             ["Transit", "Wallet"]),
            ("Booking", "form", "Reserve a desk or a court.",
             [("Place", "Harbour library"), ("When", "Thu 11:00"), ("Seats", "1")],
             ["Events", "Offices"]),
            ("Events", "list", "This week on the square.",
             [("Night market", "Thu 18:00"), ("Repair cafe", "Sat 10:00")],
             ["EventDetail", "Booking"]),
            ("EventDetail", "detail", "Harbour night market.",
             [("Where", "Yard B"), ("Stalls", "42"), ("Transit", "Bus 12")],
             ["Events", "Offices"]),
            ("News", "list", "Borough notes.",
             [("Bridge works", "Night closures from Monday"), ("Crate scheme", "Food surplus Thursdays")],
             ["ArticleDetail"]),
            ("ArticleDetail", "detail", "Bridge works — night closures.",
             [("From", "Mon 21 Sep"), ("Bus 12", "Diverted via Aurora")],
             ["News", "Transit"]),
            ("Offices", "list", "Counters still open.",
             [("Town hall", "0.6 mi · until 16:00"), ("Library", "0.3 mi · until 20:00")],
             ["Booking", "People"]),
            ("Wallet", "detail", "Civic pass + rover.",
             [("Pass", "Resident · Ada"), ("Rover", "Active today"), ("Points", "120")],
             ["TicketDetail", "Permits"]),
            ("Permits", "list", "Paper the borough issued.",
             [("Visitor bay", "Ready"), ("Skip", "Expired")],
             ["PermitDetail", "Services"]),
            ("PermitDetail", "detail", "Visitor bay — 3 days.",
             [("Bay", "Harbour Walk"), ("Starts", "Thu"), ("Fee", "£12")],
             ["Permits", "Wallet"]),
            ("People", "list", "Ward contacts.",
             [("Cllr Chen", "East quay"), ("Desk", "Waste · 020 7946 2000")],
             ["Contact", "Offices"]),
            ("Faq", "list", "What residents ask.",
             [("Bins", "Food + recycling Thursday."), ("Rover", "QR in Wallet.")],
             ["Help"]),
            ("Contact", "form", "Write the desk.",
             [("Topic", "Missed bin"), ("Message", "Food caddy still full.")],
             ["Services", "Help"]),
            ("About", "detail", "Civic Pulse · Lumina prototype.",
             [("Borough", "Harbour"), ("Build", "1.0.0"), ("Data", "Static seed")],
             ["Settings"]),
            ("Help", "list", "How to use Pulse.",
             [("Tickets", "Wallet holds the QR."), ("Requests", "Photo optional.")],
             ["Faq", "Contact"]),
            ("Notifications", "list", "Borough pings.",
             [("Bin day", "Tomorrow 07:00"), ("Bus 12", "Short delay")],
             ["Transit", "Services"]),
            ("Settings", "form", "Alerts and theme.",
             [("Bin reminder", "On"), ("Dark paper", "Off")],
             ["About", "Help", "WhatsNew"]),
            ("WhatsNew", "detail", "1.0 prototype notes.",
             [("Screens", "22 civic routes"), ("Data", "NuvexaDB seed")],
             ["About"]),
        ],
    },
]


def pascal(name: str) -> str:
    return name


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_platforms(app_dir: Path, ns: str, letter: str, accent: str, title: str) -> None:
    # Android
    write(
        app_dir / "Platforms/Android/AndroidManifest.xml",
        """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
	<application android:allowBackup="false" android:icon="@mipmap/appicon" android:roundIcon="@mipmap/appicon_round" android:supportsRtl="true"></application>
	<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
	<uses-permission android:name="android.permission.INTERNET" />
</manifest>
""",
    )
    write(
        app_dir / "Platforms/Android/MainActivity.cs",
        f"""using Android.App;
using Android.Content.PM;

namespace {ns};

[Activity(Theme = "@style/Maui.SplashTheme", MainLauncher = true, LaunchMode = LaunchMode.SingleTop,
    ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation | ConfigChanges.UiMode |
    ConfigChanges.ScreenLayout | ConfigChanges.SmallestScreenSize | ConfigChanges.Density)]
public class MainActivity : MauiAppCompatActivity
{{
}}
""",
    )
    write(
        app_dir / "Platforms/Android/MainApplication.cs",
        f"""using Android.App;
using Android.Runtime;

namespace {ns};

[Application]
public class MainApplication : MauiApplication
{{
    public MainApplication(IntPtr handle, JniHandleOwnership ownership)
        : base(handle, ownership)
    {{
    }}

    protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();
}}
""",
    )
    write(
        app_dir / "Platforms/Android/Resources/values/colors.xml",
        f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="colorPrimary">{accent}</color>
    <color name="colorPrimaryDark">#161411</color>
    <color name="colorAccent">{accent}</color>
</resources>
""",
    )
    # iOS
    write(
        app_dir / "Platforms/iOS/AppDelegate.cs",
        f"""using Foundation;

namespace {ns};

[Register("AppDelegate")]
public class AppDelegate : MauiUIApplicationDelegate
{{
    protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();
}}
""",
    )
    write(
        app_dir / "Platforms/iOS/Program.cs",
        f"""using ObjCRuntime;
using UIKit;

namespace {ns};

public class Program
{{
    static void Main(string[] args)
    {{
        UIApplication.Main(args, null, typeof(AppDelegate));
    }}
}}
""",
    )
    shutil.copyfile(UIKIT_SAMPLE / "Platforms/iOS/Info.plist", app_dir / "Platforms/iOS/Info.plist")
    privacy = TEMPLATE / "Platforms/iOS/Resources/PrivacyInfo.xcprivacy"
    if privacy.exists():
        dest = app_dir / "Platforms/iOS/Resources/PrivacyInfo.xcprivacy"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(privacy, dest)
    # Mac Catalyst
    write(
        app_dir / "Platforms/MacCatalyst/AppDelegate.cs",
        f"""using Foundation;

namespace {ns};

[Register("AppDelegate")]
public class AppDelegate : MauiUIApplicationDelegate
{{
    protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();
}}
""",
    )
    write(
        app_dir / "Platforms/MacCatalyst/Program.cs",
        f"""using ObjCRuntime;
using UIKit;

namespace {ns};

public class Program
{{
    static void Main(string[] args)
    {{
        UIApplication.Main(args, null, typeof(AppDelegate));
    }}
}}
""",
    )
    shutil.copyfile(UIKIT_SAMPLE / "Platforms/MacCatalyst/Info.plist", app_dir / "Platforms/MacCatalyst/Info.plist")
    shutil.copyfile(UIKIT_SAMPLE / "Platforms/MacCatalyst/Entitlements.plist", app_dir / "Platforms/MacCatalyst/Entitlements.plist")
    # Windows
    write(
        app_dir / "Platforms/Windows/App.xaml",
        f"""<maui:MauiWinUIApplication
    x:Class="{ns}.WinUI.App"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:maui="using:Microsoft.Maui">
</maui:MauiWinUIApplication>
""",
    )
    write(
        app_dir / "Platforms/Windows/App.xaml.cs",
        f"""namespace {ns}.WinUI;

public partial class App : MauiWinUIApplication
{{
    public App()
    {{
        this.InitializeComponent();
    }}

    protected override MauiApp CreateMauiApp() => MauiProgram.CreateMauiApp();
}}
""",
    )
    write(
        app_dir / "Platforms/Windows/app.manifest",
        f"""<?xml version="1.0" encoding="utf-8"?>
<assembly manifestVersion="1.0" xmlns="urn:schemas-microsoft-com:asm.v1">
  <assemblyIdentity version="1.0.0.0" name="{ns}.WinUI.app"/>
  <application xmlns="urn:schemas-microsoft-com:asm.v3">
    <windowsSettings>
      <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true/PM</dpiAware>
      <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2, PerMonitor</dpiAwareness>
      <longPathAware xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">true</longPathAware>
    </windowsSettings>
  </application>
</assembly>
""",
    )
    shutil.copyfile(TEMPLATE / "Platforms/Windows/Package.appxmanifest", app_dir / "Platforms/Windows/Package.appxmanifest")
    # Resources
    write(
        app_dir / "Resources/AppIcon/appicon.svg",
        f"""<svg width="456" height="456" viewBox="0 0 456 456" xmlns="http://www.w3.org/2000/svg">
  <rect width="456" height="456" rx="96" fill="{accent}"/>
  <text x="228" y="280" text-anchor="middle" font-size="180" font-family="sans-serif" fill="#FFFCF7">{letter}</text>
</svg>
""",
    )
    write(
        app_dir / "Resources/Splash/splash.svg",
        f"""<svg width="456" height="456" viewBox="0 0 456 456" xmlns="http://www.w3.org/2000/svg">
  <rect width="456" height="456" fill="#F6F1E8"/>
  <circle cx="228" cy="228" r="72" fill="{accent}"/>
</svg>
""",
    )
    write(app_dir / "Resources/Raw/AboutAssets.txt", f"{title} — Lumina prototype. Static seed in NuvexaDB.\n")
    write(
        app_dir / "App.xaml",
        f"""<?xml version="1.0" encoding="UTF-8" ?>
<Application xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="{ns}.App">
    <Application.Resources>
        <ResourceDictionary />
    </Application.Resources>
</Application>
""",
    )


def emit_core() -> None:
    proj = OUT / "src/NuvyntraLabs.Lumina.Core"
    write(
        proj / "NuvyntraLabs.Lumina.Core.csproj",
        """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <RootNamespace>NuvyntraLabs.Lumina.Core</RootNamespace>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Plugin.Maui.HttpForge" Version="1.1.1" />
    <PackageReference Include="Plugin.Maui.LocalStore" Version="1.1.0" />
  </ItemGroup>
</Project>
""",
    )
    write(
        proj / "Models/CatalogItem.cs",
        """namespace NuvyntraLabs.Lumina.Core;

public sealed class CatalogItem
{
    public string? Id { get; set; }
    public string Title { get; set; } = "";
    public string Subtitle { get; set; } = "";
    public string Group { get; set; } = "";
}
""",
    )
    write(
        proj / "Models/ChatLine.cs",
        """namespace NuvyntraLabs.Lumina.Core;

public sealed class ChatLine
{
    public string Author { get; set; } = "";
    public string Text { get; set; } = "";
}
""",
    )

    # Seed + APIs per app
    for app in APPS:
        items = []
        for name, kind, blurb, rows, _nav in app["screens"]:
            for title, subtitle in rows:
                items.append((name, title, subtitle, kind))
        item_lits = ",\n".join(
            f'            new CatalogItem {{ Id = "{app["id"].lower()}-{i:03d}", Title = {csharp_string(title)}, Subtitle = {csharp_string(subtitle)}, Group = {csharp_string(group)} }}'
            for i, (group, title, subtitle, _) in enumerate(items, 1)
        )
        write(
            proj / f"Seed/{app['id']}Seed.cs",
            f"""namespace NuvyntraLabs.Lumina.Core;

public static class {app['id']}Seed
{{
    public const string Collection = "{app['id'].lower()}";

    public static IReadOnlyList<CatalogItem> Items {{ get; }} =
    [
{item_lits}
    ];
}}
""",
        )
        iface = f"I{app['id']}Api"
        write(
            proj / f"Api/{iface}.cs",
            f"""using Plugin.Maui.HttpForge;

namespace NuvyntraLabs.Lumina.Core;

public interface {iface}
{{
    [Get("/{app['id'].lower()}/items")]
    Task<IReadOnlyList<CatalogItem>> ListAsync(CancellationToken cancellationToken = default);

    [Get("/{app['id'].lower()}/items/{{id}}")]
    Task<CatalogItem> GetAsync(string id, CancellationToken cancellationToken = default);
}}
""",
        )
        write(
            proj / f"Api/{app['id']}Api.cs",
            f"""namespace NuvyntraLabs.Lumina.Core;

public sealed class {app['id']}Api : I{app['id']}Api
{{
    public Task<IReadOnlyList<CatalogItem>> ListAsync(CancellationToken cancellationToken = default)
    {{
        cancellationToken.ThrowIfCancellationRequested();
        return Task.FromResult<IReadOnlyList<CatalogItem>>({app['id']}Seed.Items);
    }}

    public Task<CatalogItem> GetAsync(string id, CancellationToken cancellationToken = default)
    {{
        cancellationToken.ThrowIfCancellationRequested();
        var item = {app['id']}Seed.Items.FirstOrDefault(x => x.Id == id)
            ?? {app['id']}Seed.Items[0];
        return Task.FromResult(item);
    }}
}}
""",
        )

    write(
        proj / "Store/LuminaStore.cs",
        """using Plugin.Maui.LocalStore;

namespace NuvyntraLabs.Lumina.Core;

public static class LuminaStore
{
    public static async Task SeedAsync(ILocalStore store, string collection, IReadOnlyList<CatalogItem> items, CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(store);
        var col = store.GetCollection<CatalogItem>(collection);
        var existing = await col.FindAsync().ConfigureAwait(false);
        if (existing.Count > 0)
        {
            return;
        }

        await col.InsertManyAsync(items.ToList()).ConfigureAwait(false);
    }
}
""",
    )


def csharp_string(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def emit_app(app: dict) -> None:
    app_id = app["id"]
    ns = f"NuvyntraLabs.Lumina.{app_id}"
    proj_name = f"NuvyntraLabs.Lumina.{app_id}"
    app_dir = OUT / "src" / proj_name
    screens = app["screens"]
    start = app["start"]
    home = app["home"]
    names = [s[0] for s in screens]

    write(
        app_dir / f"{proj_name}.csproj",
        f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFrameworks>net10.0-android;net10.0-ios;net10.0-maccatalyst</TargetFrameworks>
    <TargetFrameworks Condition="$([MSBuild]::IsOSPlatform('windows'))">$(TargetFrameworks);net10.0-windows10.0.19041.0</TargetFrameworks>
    <OutputType>Exe</OutputType>
    <RootNamespace>{ns}</RootNamespace>
    <UseMaui>true</UseMaui>
    <SingleProject>true</SingleProject>
    <IsPackable>false</IsPackable>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <MauiXamlInflator>SourceGen</MauiXamlInflator>
    <ApplicationTitle>{app['title']}</ApplicationTitle>
    <ApplicationId>{app['app_id']}</ApplicationId>
    <ApplicationDisplayVersion>1.0.0</ApplicationDisplayVersion>
    <ApplicationVersion>1</ApplicationVersion>
    <WindowsPackageType>None</WindowsPackageType>
    <SupportedOSPlatformVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'ios'">15.0</SupportedOSPlatformVersion>
    <SupportedOSPlatformVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'maccatalyst'">15.0</SupportedOSPlatformVersion>
    <SupportedOSPlatformVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'android'">21.0</SupportedOSPlatformVersion>
    <SupportedOSPlatformVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'windows'">10.0.17763.0</SupportedOSPlatformVersion>
    <TargetPlatformMinVersion Condition="$([MSBuild]::GetTargetPlatformIdentifier('$(TargetFramework)')) == 'windows'">10.0.17763.0</TargetPlatformMinVersion>
  </PropertyGroup>
  <ItemGroup>
    <MauiIcon Include="Resources\\AppIcon\\appicon.svg" Color="{app['accent']}" />
    <MauiSplashScreen Include="Resources\\Splash\\splash.svg" Color="#F6F1E8" BaseSize="128,128" />
    <MauiAsset Include="Resources\\Raw\\**" LogicalName="%(RecursiveDir)%(Filename)%(Extension)" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Maui.Controls" Version="10.0.90" />
    <PackageReference Include="Microsoft.Extensions.Logging.Debug" Version="10.0.0" />
    <PackageReference Include="NuvyntraLabs.UIKit" Version="1.4.0" />
    <PackageReference Include="Plugin.Maui.MVVMExpress" Version="1.3.0" />
    <PackageReference Include="Plugin.Maui.MVVMExpress.Core" Version="1.3.0" />
    <PackageReference Include="Plugin.Maui.MVVMExpress.Dialogs" Version="1.3.0" />
    <PackageReference Include="Plugin.Maui.MVVMExpress.Navigation" Version="1.3.0" />
    <PackageReference Include="Plugin.Maui.MVVMExpress.SourceGenerators" Version="1.3.0">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
    <PackageReference Include="Plugin.Maui.HttpForge" Version="1.1.1" />
    <PackageReference Include="Plugin.Maui.LocalStore" Version="1.1.0" />
    <PackageReference Include="Plugin.Maui.FormValidation" Version="1.0.4" />
    <PackageReference Include="Plugin.Maui.FeatureFlags" Version="1.0.9" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\\NuvyntraLabs.Lumina.Core\\NuvyntraLabs.Lumina.Core.csproj" />
  </ItemGroup>
</Project>
""",
    )

    maps = "\n                    ".join(f'.Map<{n}ViewModel, {n}Page>("{n.lower()}")' for n in names)
    transients = "\n        ".join(
        f"builder.Services.AddTransient<{n}ViewModel>();\n        builder.Services.AddTransient<{n}Page>();" for n in names
    )
    write(
        app_dir / "MauiProgram.cs",
        f"""using Microsoft.Extensions.Logging;
using NuvyntraLabs.Lumina.Core;
using NuvyntraLabs.UIKit;
using Plugin.Maui.FeatureFlags;
using Plugin.Maui.FormValidation;
using Plugin.Maui.HttpForge;
using Plugin.Maui.LocalStore;
using Plugin.Maui.MVVMExpress.Auth;
using Plugin.Maui.MVVMExpress.Dialogs;
using Plugin.Maui.MVVMExpress.Hosting;
using Plugin.Maui.MVVMExpress.Navigation;

namespace {ns};

public static class MauiProgram
{{
    public static MauiApp CreateMauiApp()
    {{
        var builder = MauiApp.CreateBuilder();
        builder
            .UseMauiApp<App>()
            .UseNuvyntraUIKit()
            .UseMauiFormValidation(o =>
            {{
                o.Trigger = ValidationTrigger.LostFocus;
                o.ShowMessage = true;
            }})
            .UseMauiFeatureFlags(o =>
            {{
                o.Environment = FeatureFlagEnvironment.Development;
                o.LocalFlags["new_checkout"] = true;
                o.LocalFlags["telehealth"] = true;
                o.LocalFlags["offline_first"] = true;
            }})
            .UseMauiLocalStore(o =>
            {{
                o.Backend = StoreBackend.Nuvexa;
                o.Path = Path.Combine(FileSystem.AppDataDirectory, "lumina-{app_id.lower()}.nvx");
                o.CreateIfMissing = true;
            }})
            .UseHttpForge()
            .UseMvvmExpress(o => o
                .UseNavigationPage((nav, _) => nav
                    {maps})
                .UseDialogs()
                .UseAuth<SignInViewModel>());

        builder.Services.AddSingleton<IAuthState, DemoAuthState>();
        builder.Services.AddSingleton<I{app_id}Api, {app_id}Api>();
        {transients}

#if DEBUG
        builder.Logging.AddDebug();
#endif
        return builder.Build();
    }}
}}
""",
    )

    write(
        app_dir / "App.xaml.cs",
        f"""using NuvyntraLabs.Lumina.Core;
using NuvyntraLabs.UIKit;
using Plugin.Maui.LocalStore;

namespace {ns};

public partial class App : Application
{{
    readonly IServiceProvider _services;

    public App(IServiceProvider services)
    {{
        ArgumentNullException.ThrowIfNull(services);
        InitializeComponent();
        _services = services;
        NVTheme.Current.UseLumina();
        NVTheme.Current.SetAccent(Color.FromArgb("{app['accent']}"));
        NVTheme.Current.SetMode(NVThemeMode.Light);
        _ = SeedAsync();
    }}

    protected override Window CreateWindow(IActivationState? activationState)
        => new(new NavigationPage(_services.GetRequiredService<{start}Page>()));

    static async Task SeedAsync()
    {{
        try
        {{
            await LuminaStore.SeedAsync(LocalStore.Current, {app_id}Seed.Collection, {app_id}Seed.Items).ConfigureAwait(false);
        }}
        catch (Exception)
        {{
            // Prototype still runs from in-memory seed when the .nvx file cannot open.
        }}
    }}
}}
""",
    )

    write(
        app_dir / "Auth/DemoAuthState.cs",
        f"""using System.ComponentModel;
using Plugin.Maui.MVVMExpress.Auth;
using Result = Plugin.Maui.MVVMExpress.Outcome.Outcome;

namespace {ns};

public sealed class DemoAuthState : IAuthState, INotifyPropertyChanged
{{
    public const string DemoPassword = "secret";

    public bool IsAuthenticated {{ get; private set; }}
    public string? UserName {{ get; private set; }}
    public string? Email {{ get; private set; }}
    public string? DisplayName => UserName;
    public event EventHandler? Changed;
    public event PropertyChangedEventHandler? PropertyChanged;

    public Task<Result> SignInAsync(string userName, string password, CancellationToken cancellationToken = default)
    {{
        cancellationToken.ThrowIfCancellationRequested();
        if (password != DemoPassword)
        {{
            return Task.FromResult(Result.Failure("E_AUTH", "Invalid credentials — use password secret"));
        }}

        IsAuthenticated = true;
        UserName = userName.Trim();
        Email = UserName.Contains('@', StringComparison.Ordinal) ? UserName : null;
        Raise();
        return Task.FromResult(Result.Success());
    }}

    public Task SignOutAsync(CancellationToken cancellationToken = default)
    {{
        cancellationToken.ThrowIfCancellationRequested();
        IsAuthenticated = false;
        UserName = null;
        Email = null;
        Raise();
        return Task.CompletedTask;
    }}

    void Raise()
    {{
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(IsAuthenticated)));
        Changed?.Invoke(this, EventArgs.Empty);
    }}
}}
""",
    )

    write(
        app_dir / "Pages/LuminaPage.cs",
        f"""using NuvyntraLabs.UIKit;

namespace {ns};

public abstract class LuminaPage : ContentPage
{{
    protected LuminaPage(string title, string kicker, string body)
    {{
        Title = title;
        BackgroundColor = NVTheme.Current.Paper;
        var stack = new VerticalStackLayout
        {{
            Padding = new Thickness(20, 16, 20, 32),
            Spacing = NVTokens.Space3
        }};
        stack.Add(new NVCaptionText {{ Text = kicker.ToUpperInvariant() }});
        stack.Add(new NVHeading {{ Text = title, Role = NVTextRole.Title }});
        stack.Add(new NVBodyText {{ Text = body }});
        Root = stack;
        Content = new ScrollView {{ Content = stack }};
    }}

    protected VerticalStackLayout Root {{ get; }}

    protected void AddCard(string title, string body)
    {{
        Root.Add(new NVCard {{ Title = title, Body = body }});
    }}

    protected void AddAction(string text, System.Windows.Input.ICommand command, NVButtonVariant variant = NVButtonVariant.Filled)
    {{
        Root.Add(new NVButton {{ Text = text, Variant = variant, Command = command }});
    }}
}}
""",
    )

    # Fix typo in LuminaPage - I wrote Content = new ScrollView {{ Content = stack }; with missing brace
    # I'll fix after generation if needed. Let me write it correctly in a follow-up... 
    # Actually I'll fix it here by rewriting - wait I already have the typo in the string.
    # Let me fix emit - I'll patch after.

    for name, kind, blurb, rows, navs in screens:
        route = name.lower()
        commands = []
        methods = []
        for target in navs:
            if target not in names:
                continue
            async_name = f"Open{target}Async"
            cmd = f"Open{target}Command"
            commands.append(cmd)
            if target == home and name in ("SignIn", "PinLock", "Walkthrough", "ProfileSetup", "ResetPassword"):
                methods.append(
                    f"""    [AsyncModelCommand]
    private Task {async_name}(CancellationToken cancellationToken)
        => Navigator!.ResetAsync<{target}ViewModel>(cancellationToken);
"""
                )
            else:
                methods.append(
                    f"""    [AsyncModelCommand]
    private Task {async_name}(CancellationToken cancellationToken)
        => Navigator!.NavigateToAsync<{target}ViewModel>(cancellationToken);
"""
                )

        extra_fields = ""
        extra_ctor = ""
        extra_usings = ""
        if name == "SignIn":
            extra_usings = """using Plugin.Maui.MVVMExpress.Auth;
"""
            extra_fields = """
    readonly IAuthState _auth;
    [Notify] private string _email = "demo@lumina.app";
    [Notify] private string _password = DemoAuthState.DemoPassword;
"""
            extra_ctor = """
        _auth = auth;
        Email = "demo@lumina.app";
"""
            methods.insert(
                0,
                f"""    [AsyncModelCommand]
    private async Task SignInAsync(CancellationToken cancellationToken)
    {{
        var result = await _auth.SignInAsync(Email, Password, cancellationToken).ConfigureAwait(false);
        if (!result.IsSuccess)
        {{
            await Dialogs!.ErrorAsync(result.Error!, cancellationToken).ConfigureAwait(false);
            return;
        }}

        await Navigator!.ResetAsync<{home}ViewModel>(cancellationToken).ConfigureAwait(false);
    }}
""",
            )
            ctor_params = "IAuthState auth, INavigator navigator, IDialogs dialogs"
        else:
            ctor_params = "INavigator navigator, IDialogs dialogs"

        write(
            app_dir / f"ViewModels/{name}ViewModel.cs",
            f"""using Plugin.Maui.MVVMExpress.ComponentModel;
using Plugin.Maui.MVVMExpress.Dialogs;
using Plugin.Maui.MVVMExpress.Hosting;
using Plugin.Maui.MVVMExpress.Input;
using Plugin.Maui.MVVMExpress.Navigation;
{extra_usings}
namespace {ns};

[RegisterViewModel]
[Route("{route}")]
public partial class {name}ViewModel : PageViewModel
{{
{extra_fields}
    public {name}ViewModel({ctor_params})
        : base(navigator, dialogs)
    {{
{extra_ctor}
    }}

{''.join(methods)}
}}
""",
        )

        # Page
        row_adds = "\n        ".join(
            f"AddCard({csharp_string(t)}, {csharp_string(s)});" for t, s in rows
        )
        action_adds = []
        if name == "SignIn":
            action_adds.append(
                'Root.Add(new NVTextField { Label = "Email" });\n        Root.Add(new NVTextField { Label = "Password", IsPassword = true });\n        AddAction("Sign in", vm.SignInCommand);'
            )
        for target in navs:
            if target not in names:
                continue
            label = "Continue" if target == home and name in ("SignIn", "Walkthrough", "PinLock") else target
            variant = "Filled" if target == navs[0] else "Tonal" if target == home else "Outline"
            action_adds.append(
                f"AddAction({csharp_string(label)}, vm.Open{target}Command, NVButtonVariant.{variant});"
            )
        extras = ""
        if kind == "chat":
            extras = """
        Root.Add(new NVChat
        {
            Messages = rows.Select(r => new NVChatMessage { Author = r.Title, Text = r.Subtitle }).ToList()
        });
"""
        elif name in ("Home", "Dashboard"):
            extras = """
        Root.Add(new NVChart
        {
            Series =
            [
                new NVChartSeries
                {
                    Title = "This week",
                    Kind = NVChartSeriesKind.Bar,
                    Points =
                    [
                        new NVChartPoint { Category = "Mon", Value = 4 },
                        new NVChartPoint { Category = "Wed", Value = 7 },
                        new NVChartPoint { Category = "Fri", Value = 5 }
                    ]
                }
            ]
        });
"""
        elif name == "Walkthrough":
            extras = """
        Root.Add(new NVCarousel { Items = rows.Select(r => r.Title).ToList() });
        Root.Add(new NVDotIndicator { Count = 3, Index = 0 });
"""
        elif name == "PinLock":
            extras = "        Root.Add(new NVLockPad());\n"
        elif name == "InCall":
            extras = "        Root.Add(new NVInCallView());\n"
        elif name == "Booking":
            extras = "        Root.Add(new NVCalendar());\n"
        elif name == "HealthProfile":
            extras = "        Root.Add(new NVGauge { Value = 72 });\n        Root.Add(new NVAvatar { Initials = \"AL\", StatusOn = true });\n"

        write(
            app_dir / f"Pages/{name}Page.cs",
            f"""using NuvyntraLabs.Lumina.Core;
using NuvyntraLabs.UIKit;

namespace {ns};

public sealed class {name}Page : LuminaPage
{{
    public {name}Page({name}ViewModel vm) : base({csharp_string(name if name != 'Faq' else 'FAQ')}, {csharp_string(app['title'])}, {csharp_string(blurb)})
    {{
        ArgumentNullException.ThrowIfNull(vm);
        BindingContext = vm;
        var rows = {app_id}Seed.Items.Where(x => x.Group == "{name}").ToList();
        if (rows.Count == 0)
        {{
            rows = {app_id}Seed.Items.Take(3).ToList();
        }}

        foreach (var row in rows)
        {{
            AddCard(row.Title, row.Subtitle);
        }}
{extras}
        {chr(10)+'        '.join(action_adds)}
    }}
}}
""",
        )

    copy_platforms(app_dir, ns, app["letter"], app["accent"], app["title"])


def emit_docs(total: int) -> None:
    lines = ["# NuvyntraLabs.Lumina", "", "Five standalone .NET MAUI prototypes in one hub submodule. Lumina UI, MVVMExpress navigation, HttpForge contracts, NuvexaDB via LocalStore. Static seed — no live backends.", "", "## Apps", ""]
    for app in APPS:
        lines.append(f"- **{app['title']}** (`src/NuvyntraLabs.Lumina.{app['id']}`) — {app['tagline']} · {len(app['screens'])} screens")
    lines += [
        "",
        f"**{total} screens** across the five heads.",
        "",
        "## Run",
        "",
        "```bash",
        "dotnet build src/NuvyntraLabs.Lumina.Market/NuvyntraLabs.Lumina.Market.csproj -f net10.0-maccatalyst",
        "```",
        "",
        "Demo password on every sign-in screen: `secret`.",
        "",
        "## Stack",
        "",
        "- [NuvyntraLabs.UIKit](https://www.nuget.org/packages/NuvyntraLabs.UIKit) 1.4.0",
        "- [Plugin.Maui.MVVMExpress](https://www.nuget.org/packages/Plugin.Maui.MVVMExpress) 1.3.0",
        "- [Plugin.Maui.HttpForge](https://www.nuget.org/packages/Plugin.Maui.HttpForge) 1.1.1",
        "- [Plugin.Maui.LocalStore](https://www.nuget.org/packages/Plugin.Maui.LocalStore) 1.1.0 + [Nuventra.NuvexaDB](https://www.nuget.org/packages/Nuventra.NuvexaDB)",
        "- [Plugin.Maui.FormValidation](https://www.nuget.org/packages/Plugin.Maui.FormValidation) 1.0.4",
        "- [Plugin.Maui.FeatureFlags](https://www.nuget.org/packages/Plugin.Maui.FeatureFlags) 1.0.9",
        "",
        "Niladri Padhy / Nuvyntra Labs. MIT.",
        "",
    ]
    write(OUT / "README.md", "\n".join(lines))
    write(
        OUT / "AGENTS.md",
        """# NuvyntraLabs.Lumina — AI Coding Agent Guide

Five standalone MAUI apps (Market, Clinic, Field, Bank, Civic) plus `NuvyntraLabs.Lumina.Core`.

- Hub folder: `Lumina/`
- GitHub: https://github.com/nuvyntralabs/NuvyntraLabs.Lumina
- UI: `NuvyntraLabs.UIKit` (`NV*` + Lumina tokens). Do not add Syncfusion / Telerik / CommunityToolkit.Mvvm.
- Navigation: `Plugin.Maui.MVVMExpress` NavigationPage maps. ViewModels never call `Shell.Current`.
- Data: HttpForge interfaces implemented by in-memory seed; LocalStore opens a Nuvexa `.nvx` on first launch.
- Publishing: this is an app, not a nupkg. Never `dotnet nuget push`.
""",
    )
    write(OUT / "LICENSE", (ROOT / "LICENSE").read_text(encoding="utf-8"))
    write(
        OUT / ".gitignore",
        """[Bb]in/
[Oo]bj/
.vs/
*.user
.DS_Store
artifacts/
""",
    )
    write(
        OUT / "Directory.Build.props",
        """<Project>
  <PropertyGroup>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <LangVersion>latest</LangVersion>
    <MauiVersion>10.0.90</MauiVersion>
  </PropertyGroup>
</Project>
""",
    )
    write(
        OUT / "nuget.config",
        """<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" protocolVersion="3" />
  </packageSources>
</configuration>
""",
    )
    write(
        OUT / "NuvyntraLabs.Lumina.slnx",
        """<Solution>
  <Folder Name="/src/">
    <Project Path="src/NuvyntraLabs.Lumina.Core/NuvyntraLabs.Lumina.Core.csproj" />
    <Project Path="src/NuvyntraLabs.Lumina.Market/NuvyntraLabs.Lumina.Market.csproj" />
    <Project Path="src/NuvyntraLabs.Lumina.Clinic/NuvyntraLabs.Lumina.Clinic.csproj" />
    <Project Path="src/NuvyntraLabs.Lumina.Field/NuvyntraLabs.Lumina.Field.csproj" />
    <Project Path="src/NuvyntraLabs.Lumina.Bank/NuvyntraLabs.Lumina.Bank.csproj" />
    <Project Path="src/NuvyntraLabs.Lumina.Civic/NuvyntraLabs.Lumina.Civic.csproj" />
  </Folder>
</Solution>
""",
    )


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    emit_core()
    total = 0
    for app in APPS:
        emit_app(app)
        total += len(app["screens"])
    emit_docs(total)
    print(f"Wrote {OUT} with {total} screens across {len(APPS)} apps")


if __name__ == "__main__":
    main()
