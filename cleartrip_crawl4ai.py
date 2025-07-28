import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    url = "https://www.cleartrip.com/hotels/details/goverdhan-greens-resort-3936440?c=010825%7C020825&r=2%2C0"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        # ✅ Save as Markdown file
        file_name = "hotel_cleartrip.md"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(result.markdown)
        print(f"✅ Markdown saved to {file_name}")

        # (Optional) also print in console
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
