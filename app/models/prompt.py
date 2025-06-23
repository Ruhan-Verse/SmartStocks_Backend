from pydantic import BaseModel

class PromptContext(BaseModel):
    stock_data: str
    news_summary: str
    user_question: str
