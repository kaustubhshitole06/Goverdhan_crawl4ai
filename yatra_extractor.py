import re
import json

# Load the markdown file
with open("yatra_hotel.md", "r", encoding="utf-8") as f:
    content = f.read()

# Clean markdown: remove image links only
content = re.sub(r"!\[.*?\]\(.*?\)", "", content)

# Extract all relevant room blocks
room_blocks = re.findall(r"(.*?)Book Now", content, re.DOTALL)

data = {
    "hotel_name": "Goverdhan Greens Resort",
    "rooms_available": len(room_blocks),
    "room_options": []
}

for block in room_blocks:
    room = {
        "room_type": None,
        "plan": None,
        "price_per_night": 0,
        "taxes_and_fees": 0,
        "total_price": 0,
        "extras": None,
        "amenities": []
    }

    # Room Type
    match = re.search(r"\* (.*?) \[More Info", block)
    if match:
        room["room_type"] = match.group(1).strip()
    else:
        title = block.strip().split("\n")[0]
        if title and "Occupancy" in title:
            room["room_type"] = title.strip()

    # Plan
    if "Breakfast" in room["room_type"] or "breakfast" in block.lower():
        room["plan"] = "With Breakfast"
    elif "Without Food" in room["room_type"]:
        room["plan"] = "Without Food"
    else:
        room["plan"] = "Room Only"

    # Price
    final_price_match = re.search(r"Final Amount Rs\.(\d+)", block)
    if final_price_match:
        room["price_per_night"] = int(final_price_match.group(1))
        room["total_price"] = int(final_price_match.group(1))

    # Extras
    extras = []
    if "Non Refundable" in block:
        extras.append("Non Refundable")
    if "Free Breakfast" in block:
        extras.append("Free Breakfast")
    room["extras"] = ", ".join(extras) if extras else None

    # Amenities
    amenities = re.findall(r"\* (.*?)\n", block)
    room["amenities"] = [a.strip() for a in amenities if not a.lower().startswith("you save")]

    # Only add if valid price
    if room["price_per_night"] > 0 and room["total_price"] > 0:
        data["room_options"].append(room)

# Save to JSON
with open("travelguru_hotel.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ JSON saved to travelguru_hotel.json")
