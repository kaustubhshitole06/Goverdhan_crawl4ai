import re
import json

def extract_travelguru_data(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    result = {
        "hotel_name": None,
        "rooms_available": None,
        "room_options": []
    }

    # ✅ Hotel Name
    hotel_match = re.search(r"#\s*([A-Za-z0-9\s\-&]+Resort)", content)
    if hotel_match:
        result["hotel_name"] = hotel_match.group(1).strip()

    # ✅ Rooms Available (fallback to count of unique room types)
    rooms_match = re.search(r"(\d+)\s*Room\(s\) left", content)
    if rooms_match:
        result["rooms_available"] = int(rooms_match.group(1))
    else:
        result["rooms_available"] = len(set(re.findall(r"(?:Super|Superior|Family|Villa|Full).+?(?=\n)", content)))

    # ✅ Extract Room Sections
    room_blocks = re.split(r"(?=\n(?:Super|Superior|Family|First Floor|Ground Floor|Full).+?Occupancy|\nVilla\s+\d+|\nFull Villa)", content)

    for sec in room_blocks:
        sec = sec.strip()
        if not sec or "Final Amount" not in sec:
            continue

        # ✅ Room Name (first line)
        room_name = sec.split("\n")[0].strip()

        # ✅ Amenities (before Room Policy)
        amenities_match = re.search(r"Amenities\s+(.*?)Room Policy", sec, re.S)
        amenities = [a.strip() for a in re.findall(r"\*\s*([A-Za-z0-9\s\.\-]+)", amenities_match.group(1))] if amenities_match else []

        # ✅ Extract Each Plan (Final Amount Correctly)
        plans = re.finditer(
            r"(Room Only|Room with Breakfast|Without Food|With Breakfast).*?"
            r"Final Amount\s*Rs\.([\d,]+).*?"
            r"Highlights\s+(.*?)Price for 1 night",
            sec,
            re.S
        )

        for p in plans:
            plan, price, highlights = p.groups()
            price = int(price.replace(",", ""))

            # ✅ Extract Extras
            extras = []
            if "Free Breakfast" in highlights:
                extras.append("Free Breakfast")
            if "Non Refundable" in highlights:
                extras.append("Non Refundable")

            result["room_options"].append({
                "room_name": room_name,
                "plan": plan.strip(),
                "price_per_night": price,
                "taxes_and_fees": 0,  # Travelguru shows final amount inclusive
                "total_price": price,
                "extras": ", ".join(extras) if extras else "None",
                "amenities": amenities
            })

    return result


# ✅ Run & Save
data = extract_travelguru_data("hotel_travelguru.md")
with open("travelguru_hotel.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(json.dumps(data, indent=4, ensure_ascii=False))
print("✅ JSON saved to travelguru_hotel.json")
