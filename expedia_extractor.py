import re
import json
import pandas as pd

def is_valid_room_name(name):
    bad_keywords = [
        "view all photos", "common areas", "check-in", "check-out", "special check-in",
        "access methods", "pets", "children", "payment", "optional extras", "you need to know",
        "we should mention", "reviews", "terrible", "okay", "poor", "good",
        "change search", "prices are typical", "where is", "how much", "what time", "does", "is", "!["
    ]
    name_lower = name.lower()
    return not any(keyword in name_lower for keyword in bad_keywords)

def extract_room_data_from_md(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    room_blocks = re.split(r"^### ", content, flags=re.MULTILINE)
    room_data = []

    for block in room_blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue

        room_name = lines[0].strip()

        if not is_valid_room_name(room_name):
            continue
        if room_name.strip().lower() == "royal villa, 4 bedrooms":
            continue  # skip this specific room

        # Extract all prices
        prices = re.findall(r"₹[\d,]+", block)
        prices = [p.replace("₹", "").replace(",", "") for p in prices]

        # Extract total price separately
        total_match = re.search(r"₹[\d,]+\s+total", block)
        total_price = None
        if total_match:
            total_price = re.search(r"₹([\d,]+)", total_match.group()).group(1).replace(",", "")
            if total_price in prices:
                prices.remove(total_price)

        # Use the last remaining price as base price (per night)
        price_per_night = prices[-1] if prices else None

        # Extract taxes & fees
        taxes_match = re.search(r"₹[\d,]+\s+taxes.*fees", block, re.IGNORECASE)
        taxes_and_fees = None
        if taxes_match:
            taxes_and_fees = re.search(r"₹([\d,]+)", taxes_match.group()).group(1).replace(",", "")

        # Extract extras like breakfast, wifi, etc.
        extras = []
        extras_patterns = [
            "free wifi", "breakfast included", "free breakfast", "non-refundable", "fully refundable",
            "air conditioning", "no meals", "free cancellation"
        ]
        for pattern in extras_patterns:
            if re.search(pattern, block, re.IGNORECASE):
                extras.append(pattern.title())

        room_data.append({
            "room_type": room_name,
            "price_per_night": int(price_per_night) if price_per_night else None,
            "taxes_and_fees": int(taxes_and_fees) if taxes_and_fees else None,
            "total_price": int(total_price) if total_price else None,
            "current_price": int(price_per_night) if price_per_night else None,
            "extras": extras,
            "amenities": []  # Can be added later if needed
        })

    return room_data

# Run extraction
markdown_path = "expedia_output.md"
room_data = extract_room_data_from_md(markdown_path)

# Save to JSON
with open("expedia_parsed_output.json", "w", encoding="utf-8") as f:
    json.dump(room_data, f, indent=2, ensure_ascii=False)

# Save to Excel
df = pd.DataFrame(room_data)
df.to_excel("expedia_parsed_output.xlsx", index=False)

print("✅ Room details (price, tax, extras) saved to JSON and Excel.")
