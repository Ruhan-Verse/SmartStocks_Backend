
import asyncio
from app.services.fetchers import gnews
print(asyncio.run(gnews.get_company_news("Tesla", count=10)))
