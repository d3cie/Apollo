from fastapi import FastAPI, HTTPException
from models.schemas import ResearchQuery, ResearchReport
from core.question_generator import QuestionGenerator
from core.search_engine import SearchEngine
from core.content_analyzer import ContentAnalyzer
from core.report_compiler import ReportCompiler
from config.settings import settings
from crawl4ai import AsyncWebCrawler, LLMExtractionStrategy

app = FastAPI()

# Initialize services
question_generator = QuestionGenerator(api_key=settings.OPENAI_API_KEY)
search_engine = SearchEngine(serp_api_key=settings.SERP_API_KEY)
content_analyzer = ContentAnalyzer(api_key=settings.GOOGLE_API_KEY)
report_compiler = ReportCompiler(
    openai_key=settings.OPENAI_API_KEY, google_api_key=settings.GOOGLE_API_KEY
)


@app.post("/research/", response_model=ResearchReport)
async def conduct_research(query: ResearchQuery):
    try:
        # Generate fewer initial questions for testing
        main_questions = await question_generator.generate_initial_questions(
            query.topic, 
            max_questions=2  # Reduced from 5 to 2
        )

        # Limit depth of sub-questions
        for question in main_questions:
            await question_generator.generate_sub_questions(
                question, 
                depth=1  # Reduced depth to 1 level
            )

        # Search and analyze content
        async with AsyncWebCrawler(verbose=True) as crawler:
            for question in main_questions:
                # Limited search results
                sources = await search_engine.search(question.text, num_results=2)
                
                # Add basic content filtering
                filtered_sources = [
                    source for source in sources 
                    if len(source.get("snippet", "")) > 100  # Only process substantial snippets
                ]
                question.sources = filtered_sources[:2]  # Limit to 2 sources

                # Extract and analyze content with character limits
                for source in question.sources:
                    try:
                        # Extract content using crawl4ai with limits
                        result = await crawler.arun(
                            url=source["link"],
                            extraction_strategy=LLMExtractionStrategy(
                                provider="gemini/gemini-1.5-pro",
                                api_token=settings.GOOGLE_API_KEY,
                                extraction_type="summary",
                                instruction=f"""
                                Extract only the most relevant information for: {question.text}
                                Limit response to 250 words.
                                Focus on factual content only.
                                """,
                                max_tokens=500  # Add token limit
                            )
                        )
                        
                        # Analyze content with limits
                        analysis = await content_analyzer.analyze_content(
                            result.extracted_content[:1000],  # Limit content length
                            question.text
                        )
                        
                        source.update({
                            "extracted_content": result.extracted_content[:1000],  # Limit stored content
                            "analysis": analysis
                        })
                    except Exception as e:
                        print(f"Error processing source {source['link']}: {str(e)}")
                        continue

        # Compile final report
        report = await report_compiler.compile_report(query.topic, main_questions)
        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
