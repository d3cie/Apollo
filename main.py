from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from typing import Optional, Dict
from crawl4ai import AsyncWebCrawler, LLMExtractionStrategy
import asyncio

load_dotenv()

# Initialize FastAPI app
app = FastAPI()


class CrawlRequest(BaseModel):
    url: str
    word_count_threshold: int = 1
    custom_instruction: Optional[str] = None


# Define response model
class CrawlResponse(BaseModel):
    url: str
    extracted_content: str
    status: str


# Basic root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/crawl/", response_model=CrawlResponse)
async def crawl_website(request: CrawlRequest):
    try:
        # Default instruction if none provided
        instruction = (
            request.custom_instruction
            or """
            Analyze the content and provide a comprehensive summary including:
            1. Main topic or purpose of the page
            2. Key points or features
            3. Any relevant data or statistics
            Please structure the information clearly.
        """
        )

        # Initialize crawler
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(
                url=request.url,
                word_count_threshold=request.word_count_threshold,
                extraction_strategy=LLMExtractionStrategy(
                    provider="openai/gpt-4o",
                    api_token=os.getenv("OPENAI_API_KEY"),
                    extraction_type="summary",
                    instruction=instruction,
                ),
                bypass_cache=True,
            )

        # Prepare response
        response = CrawlResponse(
            url=request.url,
            extracted_content=result.extracted_content,
            status="success",
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
