import re
import json
import pandas as pd
import difflib

def extract_rooms(md_text):
    # Split by room headings (###)
    room_sections = re.split(r'\n###\s+', md_text)
    rooms = []
    for section in room_sections:
        lines = section.strip().splitlines()
        if not lines:
            continue
        room_type = lines[0].strip()
        # Extract type rate (₹xxxx/night or ₹xxxx\n)
        rate_match = re.search(r'₹([\d,]+)\s*/night', section)
        if not rate_match:
            rate_match = re.search(r'₹([\d,]+)\n', section)
        type_rate = int(rate_match.group(1).replace(',', '')) if rate_match else None
        # Extract room tax
        tax_match = re.search(r'\+₹([\d,]+) taxes & fees', section)
        room_tax = int(tax_match.group(1).replace(',', '')) if tax_match else 0
        # Calculate total price
        total_price = type_rate + room_tax if type_rate else None
        # Extract amenities
        amenities = []
        amenity_matches = re.findall(r'\*\*(.*?)\*\*', section)
        for amenity in amenity_matches:
            amenities.append(amenity.strip())
        # Only add if room_type and type_rate found
        if room_type and type_rate:
            rooms.append({
                "Room Type": room_type,
                "Type Rate": type_rate,
                "Room Tax": room_tax,
                "Total Price": total_price,
                "Amenities": amenities
            })
    return rooms

# 🔹 Room mapping logic
standard_room_names = {
    "Super Deluxe Balcony - Double Occupancy": "Super Deluxe balcony",
    "Super Deluxe - Double Occupancy": "super deluxe room",
    "Deluxe Room With Balcony - Double Occupancy": "deluxe room with balcony",
    "Superior Room - Double Occupancy": "superior  room",
    "Family Deluxe Room": "family room 4 - beds",
    "First Floor Villa 2 Bedrooms": "1st floor villa with balcony",
    "Ground Floor Villa 2 BHK": "ground floor villa with kitchen",
    "Full Villa 4 BHK": "full villa 4bhk"
}

IGNORE_SUFFIXES = [
    "Room Only", "Breakfast", "With Breakfast", "Without Food",
    "Room With Breakfast", "Only", "With Food"
]

def clean_room_name(name):
    for suffix in IGNORE_SUFFIXES:
        name = re.sub(re.escape(suffix), "", name, flags=re.IGNORECASE)
    return name.strip().lower()

def map_room_fuzzy(raw_name):
    cleaned = clean_room_name(raw_name)
    best_match = None
    best_score = 0
    for base in standard_room_names:
        ratio = difflib.SequenceMatcher(None, cleaned, base.lower()).ratio()
        if ratio > best_score:
            best_match = base
            best_score = ratio
    if best_score >= 0.8:  # 80% threshold
        return standard_room_names[best_match]
    return raw_name  # fallback

if __name__ == "__main__":
    with open("yatra_hotel.md", encoding="utf-8") as f:
        md_text = f.read()

    rooms = extract_rooms(md_text)

    # 🔹 Add mapped room name
    for room in rooms:
        room["Mapped Room Type"] = map_room_fuzzy(room["Room Type"])

    # 🔹 Save as JSON
    with open("room_data.json", "w", encoding="utf-8") as jf:
        json.dump(rooms, jf, indent=4, ensure_ascii=False)
    print("✅ Saved to room_data.json")

    # 🔹 Save as Excel
    df = pd.DataFrame(rooms)
    df['Amenities'] = df['Amenities'].apply(lambda x: ', '.join(x))
    df.to_excel("room_data.xlsx", index=False)
    print("✅ Saved to room_data.xlsx")
