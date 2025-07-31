# Install with: pip install firecrawl-py
import asyncio
from firecrawl import AsyncFirecrawlApp

async def main():
    app = AsyncFirecrawlApp(api_key='fc-d59a27e925da4ad2ad1743d349859ef8')

    response = await app.scrape_url(
        url='https://www.expedia.co.in/Dwarka-Hotels-Goverdhan-Greens-Resort-Dwarka.h18105883.Hotel-Information?chkin=2025-09-11&chkout=2025-09-12&x_pwa=1&rfrr=HSR&pwa_ts=1753976821810&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jby5pbi9Ib3RlbC1TZWFyY2g%3D&useRewards=true&rm1=a2&regionId=6153892&destination=Dwarka%2C+Gujarat%2C+India&destType=MARKET&selected=18105883&latLong=22.244198%2C68.968453&sort=RECOMMENDED&top_dp=3036&top_cur=INR&userIntent=&selectedRoomType=201936146&selectedRatePlan=209816736&searchId=6289e25c-a2a2-418c-810d-6411634d9c8a',
        formats=['markdown'],
        only_main_content=True,
        parse_pdf=True
    )

    markdown_content = response.markdown  # ✅ Correct way
    with open("expedia_output.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print("✅ Markdown saved to expedia_output.md")

asyncio.run(main())
