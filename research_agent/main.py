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
    openai_key=settings.OPENAI_API_KEY,
    google_api_key=settings.GOOGLE_API_KEY
)

@app.post("/research/", response_model=ResearchReport)
async def conduct_research(query: ResearchQuery):
    try:
        # Generate questions using OpenAI
        main_questions = await question_generator.generate_initial_questions(
            query.topic, 
            query.max_questions
        )

        # Generate sub-questions
        for question in main_questions:
            await question_generator.generate_sub_questions(
                question, 
                depth=query.depth
            )

        # Search and analyze content
        async with AsyncWebCrawler(verbose=True) as crawler:
            for question in main_questions:
                # Search for sources
                sources = await search_engine.search(question.text)
                question.sources = sources

                # Extract and analyze content
                for source in sources:
                    # Extract content using crawl4ai
                    result = await crawler.arun(
                        url=source["link"],
                        extraction_strategy=LLMExtractionStrategy(
                            provider="vertex_ai",
                            extraction_type="summary",
                            instruction=f"Extract information relevant to: {question.text}"
                        )
                    )
                    
                    # Analyze content using Vertex AI
                    analysis = await content_analyzer.analyze_content(
                        result.extracted_content,
                        question.text
                    )
                    
                    source.update({
                        "extracted_content": result.extracted_content,
                        "analysis": analysis
                    })

        # Compile final report using both OpenAI and Vertex AI
        report = await report_compiler.compile_report(query.topic, main_questions)
        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 