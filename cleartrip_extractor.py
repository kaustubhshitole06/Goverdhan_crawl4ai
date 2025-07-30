import re, json

# Room mapping dictionary
ROOM_MAPPING = {
    "Super Deluxe Room with Balcony": "Super Deluxe Room with Balcony",
    "Super Deluxe Room": "AC super deluxe",
    "Deluxe Room with Balcony": "Deluxe Room with Balcony",
    "Superior Room": "Superior Room",
    "AC Family Deluxe Room": "family room 4 beds"
}

def clean_text(text):
    return re.sub(r"!\[.*?\]\(.*?\)", "", text).strip()

def extract_travelguru_data(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    result = {
        "hotel_name": None,
        "rating": None,
        "rooms_available": None,
        "room_options": []
    }

    # ✅ Hotel Name
    hotel = re.search(r"#\s*([A-Za-z0-9\s\-&]+Resort)", content)
    if hotel:
        result["hotel_name"] = hotel.group(1).strip()

    # ✅ Rating
    rating = re.search(r"###\s*([\d.]+)", content)
    if rating:
        try:
            result["rating"] = float(rating.group(1))
        except:
            result["rating"] = None

    # ✅ Rooms Available
    rooms = re.search(r"(\d+)\s+room types", content)
    if rooms:
        result["rooms_available"] = int(rooms.group(1))

    # ✅ Extract Room Sections
    room_blocks = re.split(r"####\s+(?=[A-Z].+Room)", content)
    for block in room_blocks:
        if "Room" not in block:
            continue

        lines = block.splitlines()
        room_name = clean_text(lines[0]).strip()

        # Amenities (before "Room Only" or "Room with Breakfast")
        amenities = []
        for line in lines[1:]:
            if "Room Only" in line or "Room with Breakfast" in line:
                break
            if re.search(r"[A-Za-z]", line) and "Room" not in line:
                amenities.append(clean_text(line))

        # Room Types and Prices
        price_pattern = re.findall(
            r"(Room Only|Room with Breakfast).*?₹([\d,]+)\s*\+\s*₹([\d,]+)\s*taxes",
            block, re.S
        )
        for rtype, price, taxes in price_pattern:
            try:
                p = int(price.replace(",", ""))
                t = int(taxes.replace(",", ""))
                extras = "Free cancellation" if "Free cancellation" in block else ""
                standard_room_name = ROOM_MAPPING.get(room_name, room_name)
                result["room_options"].append({
                    "room_name": room_name,
                    "standard_room_name": standard_room_name,
                    "room_type": rtype.strip(),
                    "price_per_night": p,
                    "taxes_and_fees": t,
                    "total_price": p + t,
                    "extras": extras,
                    "amenities": amenities
                })
            except:
                continue

    return result

# ✅ Run & Save JSON
data = extract_travelguru_data("hotel_cleartrip.md")
with open("cleartrip_hotel.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(json.dumps(data, indent=4, ensure_ascii=False))
print("✅ JSON saved to cleartrip_hotel.json")
