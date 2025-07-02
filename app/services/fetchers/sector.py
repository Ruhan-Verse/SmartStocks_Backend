# ✅ sector.py (updated) in app/services/fetchers/
import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://www.tradingview.com/markets/stocks-usa/sectorandindustry-sector/"

async def get_sector_performance():
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            sectors = []
            # TradingView tables often have sector rows in <tr> elements
            # Update selector based on inspecting TradingView page structure
            for row in soup.select('table tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    sector_name = cols[0].get_text(strip=True)
                    sector_change = cols[1].get_text(strip=True)
                    sectors.append({"sector": sector_name, "change": sector_change})
            return sectors
        raise Exception("Failed to fetch sector data")

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(get_sector_performance())
    print(result)
