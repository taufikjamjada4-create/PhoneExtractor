import pytesseract, re, os, cv2
from PIL import Image
import numpy as np
import openpyxl

# ✅ Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\taufi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# ✅ Clean and sharpen image
def preprocess(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return Image.fromarray(thresh)

# ✅ Phone number pattern
phone_pattern = re.compile(r'(\+?\d[\d\s\-().]{7,15}\d)')

frames_folder = "frames"
found_numbers = []

total_frames = len([f for f in os.listdir(frames_folder) if f.endswith(".jpg")])
current = 0

print(f"Scanning {total_frames} frames for phone numbers...\n")

# ✅ Scan all frames
for filename in sorted(os.listdir(frames_folder)):
    if filename.endswith(".jpg"):
        current += 1
        print(f"Scanning {current}/{total_frames} - {filename}", end="\r")

        img = preprocess(os.path.join(frames_folder, filename))
        text = pytesseract.image_to_string(img)

        for match in phone_pattern.findall(text):
            cleaned = match.strip()
            if not any(d['number'] == cleaned for d in found_numbers):
                found_numbers.append({
                    'number': cleaned,
                    'frame': filename,
                })
                print(f"\n📞 FOUND in {filename}: {cleaned}")

# ✅ Save to TEXT file
txt_path = "found_numbers.txt"
with open(txt_path, "w") as f:
    f.write("Phone Numbers Found\n")
    f.write("=" * 30 + "\n")
    for item in found_numbers:
        f.write(f"Number : {item['number']}\n")
        f.write(f"Frame  : {item['frame']}\n")
        f.write("-" * 30 + "\n")
print(f"\n✅ Saved to {txt_path}")

# ✅ Save to EXCEL file
excel_path = "found_numbers.xlsx"
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Phone Numbers"

# Header row
ws.append(["No.", "Phone Number", "Found In Frame"])

# Data rows
for i, item in enumerate(found_numbers, start=1):
    ws.append([i, item['number'], item['frame']])

# Make columns wider
ws.column_dimensions['A'].width = 5
ws.column_dimensions['B'].width = 25
ws.column_dimensions['C'].width = 25

wb.save(excel_path)
print(f"✅ Saved to {excel_path}")

# ✅ Final Summary
print(f"\n{'='*30}")
print(f"Scan Complete!")
print(f"{'='*30}")
if found_numbers:
    print(f"✅ Total unique numbers found: {len(found_numbers)}")
    for item in found_numbers:
        print(f"   📞 {item['number']}  (in {item['frame']})")
else:
    print("❌ No phone numbers found.")
print(f"{'='*30}")
print(f"📄 Text file  : D:\\PhoneExtractor\\found_numbers.txt")
print(f"📊 Excel file : D:\\PhoneExtractor\\found_numbers.xlsx")