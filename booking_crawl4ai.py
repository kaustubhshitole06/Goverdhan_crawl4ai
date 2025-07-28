import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    url = "https://www.booking.com/hotel/in/goverdhan-greens-resort.en-gb.html?aid=397594&label=gog235jc-10CAEoggI46AdIM1gDaGyIAQGYATO4ARfIAQzYAQPoAQH4AQGIAgGoAgG4AprimMQGwAIB0gIkOTQxMGYyZjUtYzRjOS00YmIxLWJhN2QtZThhNTYwOTY2ZTQy2AIB4AIB&sid=20f92286cdc30e8b57db1134e54be103&all_sr_blocks=196009803_410216187_3_42_0&checkin=2025-09-17&checkout=2025-09-18&dest_id=1960098&dest_type=hotel&dist=0&group_adults=2&group_children=0&hapos=1&highlighted_blocks=196009803_410216187_3_42_0&hpos=1&matching_block_id=196009803_410216187_3_42_0&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&sr_pri_blocks=196009803_410216187_3_42_0__412818&srepoch=1753625159&srpvid=4f70631fcab403fd&type=total&ucfs=1&"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        # ✅ Save as Markdown file
        file_name = "booking_hotel.md"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(result.markdown)
        print(f"✅ Markdown saved to {file_name}")

        # (Optional) also print in console
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
