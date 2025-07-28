import asyncio
import re
from crawl4ai import AsyncWebCrawler

def clean_markdown(content: str) -> str:
    # ✅ Remove only image links ![alt](url), keep normal hyperlinks as is
    content = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", content)

    # ✅ Remove extra blank lines
    content = re.sub(r"\n\s*\n", "\n", content)

    return content.strip()

async def main():
    url = "https://hotels.travelguru.com/hotel-search/tgdom/details?checkoutDate=29/08/2025&checkinDate=28/08/2025&roomRequests[0].id=1&roomRequests[0].noOfAdults=2&roomRequests[0].noOfChildren=0&source=BOOKING_ENGINE&tenant=TGB2C&city.name=Dwarka&city.code=Dwarka&country.name=India&country.code=IND&hotelId=00014691"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        # ✅ Clean Markdown (only images removed)
        cleaned_content = clean_markdown(result.markdown)

        # ✅ Save Clean Markdown
        file_name = "hotel_travelguru.md"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(cleaned_content)

        print(f"✅ Clean Markdown saved to {file_name}\n")
        print(cleaned_content[:2000])  # Preview first 2000 chars

if __name__ == "__main__":
    asyncio.run(main())
