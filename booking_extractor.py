import json, re

# Mapping dictionary
ROOM_MAPPING = {
    "Deluxe Double Room": "Deluxe room with balcony",
    "Super Deluxe Room with Balcony": "Super Deluxe Room with Balcony",
    "Deluxe King Room": "AC Super Deluxe",
    "Superior Double Room": "Superior",
    "Deluxe Family Room": "Family room 4 Beds",
    "Two-Bedroom Villa": "1st floor Villa with balcony",
    "Villa with Garden View": "ground floor villa with kitchen",
    "Superior Villa": "full villa 4 bhk"
}

def parse_booking_markdown(file_path="booking_hotel.md"):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    hotel_data = {
        "hotel_name": "Goverdhan Greens Resort",
        "rating": None,
        "rooms_available": 0,
        "room_options": []
    }

    room_sections = re.findall(
        r"(\[[^\]]+\][\s\S]*?Max persons:\s*\d+[\s\S]*?)(?=\n\[|$)", content
    )

    for section in room_sections:
        room_type_match = re.match(r"\[([A-Za-z0-9\s\-]+)\]", section)
        room_type = room_type_match.group(1).strip() if room_type_match else None
        if not room_type or "skip to" in room_type.lower() or "fine print" in room_type.lower():
            continue

        max_persons = int(re.search(r"Max persons:\s*(\d+)", section).group(1))

        price_match = re.search(r"(Current price|Price)\s*₹\s*([\d,]+)", section)
        price_per_night = int(price_match.group(2).replace(",", "")) if price_match else None

        taxes_match = re.search(r"\+\₹\s*([\d,]+)\s*taxes", section)
        taxes_and_fees = int(taxes_match.group(1).replace(",", "")) if taxes_match else 0

        total_match = re.search(r"Total\s*₹\s*([\d,]+)", section)
        total_price = (
            float(total_match.group(1).replace(",", "")) if total_match
            else (price_per_night + taxes_and_fees if price_per_night else None)
        )

        extras = [tag for tag in [
            "Early Booker Deal",
            "Free cancellation",
            "Pay the property before arrival",
            "Fully refundable",
            "No credit card needed"
        ] if tag in section]

        amenities = [
            f"{bed[0].strip()}: {bed[1].strip()}"
            for bed in re.findall(r"\*\*\s*([^:]+):\s*\*\*\s*([^|\n]+)", section)
        ]
        if "Continental breakfast included" in section:
            amenities.append("Breakfast included")
        elif "Breakfast ₹" in section:
            bf = re.search(r"Breakfast\s*₹\s*\d+", section)
            if bf: amenities.append(bf.group())

        meals = {
            "breakfast": "Breakfast included" if "Continental breakfast included" in section
                        else (re.search(r"Breakfast\s*₹\s*\d+", section).group() if re.search(r"Breakfast\s*₹\s*\d+", section) else None),
            "lunch": f"Lunch costs ₹ {re.search(r'Lunch costs ₹\s*(\d+)', section).group(1)}" if "Lunch costs" in section else None,
            "dinner": f"Dinner costs ₹ {re.search(r'Dinner costs ₹\s*(\d+)', section).group(1)}" if "Dinner costs" in section else None
        }

        cancellation_match = re.search(r"Free cancellation[^\\n]*", section)
        cancellation = cancellation_match.group(0).strip() if cancellation_match else None

        prepayment = "Pay the property before arrival" if "Pay the property before arrival" in section else None

        hotel_data["room_options"].append({
            "room_type": room_type,
            "standard_room_name": ROOM_MAPPING.get(room_type, room_type),  # mapping added
            "max_persons": max_persons,
            "price_per_night": price_per_night,
            "taxes_and_fees": taxes_and_fees,
            "total_price": total_price,
            "extras": extras,
            "amenities": amenities,
            "meals": meals,
            "cancellation": cancellation,
            "prepayment": prepayment
        })

    hotel_data["rooms_available"] = len(hotel_data["room_options"])
    return hotel_data


if __name__ == "__main__":
    data = parse_booking_markdown("booking_hotel.md")

    # ✅ Save JSON to file
    with open("booking_output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✅ JSON saved to booking_output.json")
