import json
import asyncio
from firecrawl import AsyncFirecrawlApp

async def main():
    app = AsyncFirecrawlApp(api_key='fc-279a26430c5f41d0bc96aa69b56d875b')
    response = await app.scrape_url(
        url='https://www.goibibo.com/hotels/hotel-details/?checkin=2025-07-12&checkout=2025-07-13&roomString=1-2-0&searchText=Goverdhan%20Greens&locusId=CTXOP&locusType=city&cityCode=CTXOP&cc=IN&_uCurrency=INR&vcid=8369616161009722573&giHotelId=2259653877757301726&mmtId=201203212233088600&topHtlId=201203212233088600&sType=hotel',
        formats=['markdown', 'screenshot@fullPage'],
        only_main_content=True,
        include_tags=["div[data-testid='detail-roomSelection-room']"],
        parse_pdf=False
    )

    output_data = {
        "markdown": response.markdown,
        "screenshot": response.screenshot
    }

    with open("firecrawl_output.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print("✅ Output saved to firecrawl_output.json")

# ✅ Use asyncio.run() to run async main function
if __name__ == "__main__":
    asyncio.run(main())
