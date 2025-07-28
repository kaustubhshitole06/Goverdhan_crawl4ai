import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    url = "https://hotel.yatra.com/nextui/hotel-detail?checkoutDate=19%2F08%2F2025&checkinDate=18%2F08%2F2025&source=BOOKING_ENGINE&pg=1&tenant=B2C&isPersnldSrp=1&city.name=Dwarka&city.code=Dwarka&state.name=Dwarka&state.code=Dwarka&country.name=IND&country.code=IND&roomRequests%5B0%5D.id=1&roomRequests%5B0%5D.noOfAdults=2&roomRequests%5B0%5D.noOfChildren=0&hotelId=00014691&propertySource=TGU"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        # ✅ Save as Markdown file
        file_name = "yatra_hotel.md"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(result.markdown)
        print(f"✅ Markdown saved to {file_name}")

        # (Optional) also print in console
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
