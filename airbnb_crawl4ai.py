import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    url = "https://www.airbnb.co.in/rooms/1119198480825500272?source_impression_id=p3_1753716577_P3-6LkU4pcyr7Xqn&guests=2&adults=2&check_in=2025-08-17&check_out=2025-08-18"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        # ✅ Save as Markdown file
        file_name = "hotel_airbnb.md"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(result.markdown)
        print(f"✅ Markdown saved to {file_name}")

        # (Optional) also print in console
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
