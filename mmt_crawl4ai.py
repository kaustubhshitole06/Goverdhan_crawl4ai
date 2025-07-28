import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    url = "https://www.makemytrip.com/hotels/hotel-details/?hotelId=201203212233088600&_uCurrency=INR&checkin=10142025&checkout=10152025&city=CTXOP&country=IN&lat=22.19207&lng=69.01994&locusId=CTXOP&locusType=city&rank=1&regionNearByExp=3&roomStayQualifier=2e0e&rsc=1e2e0e&searchText=Goverdhan+Greens&topHtlId=201203212233088600&mtkeys=undefined&isPropSearch=T"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        # ✅ Save as Markdown file
        file_name = "makemytrip_hotel.md"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(result.markdown)
        print(f"✅ Markdown saved to {file_name}")

        # (Optional) also print in console
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
