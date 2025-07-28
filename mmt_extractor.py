import re
import json

def clean_text(text):
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)  # Remove image links
    return text.strip()

def extract_hotel_data_from_markdown(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    result = {
        "hotel_name": None,
        "rating": None,
        "rooms_available": None,
        "room_options": []
    }

    current_main_room = None
    current_sub_room = None
    current_block = []

    # ✅ First Pass - Basic info
    content = "".join(lines)
    hotel = re.search(r"#\s+([^\n]+)", content)
    if hotel:
        result["hotel_name"] = hotel.group(1).strip()

    rating = re.search(r"(\d\.\d)\s+(Very Good|Excellent|Average|Good)", content)
    if rating:
        result["rating"] = float(rating.group(1))

    rooms = re.search(r"(\d+)\s+More Options", content)
    if rooms:
        result["rooms_available"] = int(rooms.group(1))

    # ✅ Line-by-line Parsing
    for line in lines:
        line = line.strip()

        if line.startswith("## "):  # Main Room Name
            current_main_room = clean_text(line.replace("##", "").strip())
            continue

        if line.startswith("##### "):  # Sub-room type
            # Process the previous block before resetting
            if current_sub_room and current_block:
                process_block(result, current_main_room, current_sub_room, current_block)
            current_sub_room = clean_text(line.replace("#####", "").strip())
            current_block = []
            continue

        if current_sub_room:
            current_block.append(line)

    # ✅ Process the last block
    if current_sub_room and current_block:
        process_block(result, current_main_room, current_sub_room, current_block)

    return result

def process_block(result, main_room, sub_room, block_lines):
    block_text = "\n".join(block_lines)

    prices = re.findall(r"₹\s*([\d,]+)\s*\n\+₹\s*([\d,]+)", block_text)
    extras = "Free Cancellation" if "Free Cancellation" in block_text else ""
    amenities = []
    if "Free Breakfast" in block_text:
        amenities.append("Free Breakfast")
    if "No meals included" in block_text:
        amenities.append("No meals included")

    for price, tax in prices:
        try:
            p = int(price.replace(",", ""))
            t = int(tax.replace(",", ""))
            result["room_options"].append({
                "main_room_name": main_room,
                "room_type": f"{main_room} - {sub_room}",
                "price_per_night": p,
                "taxes_and_fees": t,
                "total_price": p + t,
                "extras": extras,
                "amenities": amenities
            })
        except:
            continue

# ✅ Run & Save JSON
data = extract_hotel_data_from_markdown("makemytrip_hotel.md")
with open("makemytrip_hotel.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(json.dumps(data, indent=4, ensure_ascii=False))
print("✅ JSON saved to makemytrip_hotel.json")
