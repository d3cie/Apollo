from openai import AsyncOpenAI
import google.generativeai as genai
from models.schemas import ResearchReport, Question
from typing import List


class ReportCompiler:
    def __init__(self, openai_key: str, google_api_key: str):
        self.openai_client = AsyncOpenAI(api_key=openai_key)
        genai.configure(api_key=google_api_key)
        self.gemini_model = genai.GenerativeModel("gemini-1.5-pro")

    async def compile_report(
        self, topic: str, questions: List[Question]
    ) -> ResearchReport:
        # Use Gemini for initial content analysis
        analysis_prompt = self._prepare_analysis_prompt(topic, questions)
        initial_analysis = await self.gemini_model.generate_content_async(
            analysis_prompt
        )

        # Use GPT-4 for final report generation
        final_prompt = f"""
        Based on the following analysis and research data, create a comprehensive report:
        
        Initial Analysis:
        {initial_analysis.text}
        
        Topic: {topic}
        
        Create a detailed report with:
        1. Executive Summary
        2. Key Findings for each main question
        3. Detailed Analysis with citations
        4. Conclusions and Implications
        """

        response = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.7,
        )

        report_content = response.choices[0].message.content

        return ResearchReport(
            topic=topic,
            main_questions=questions,
            summary=report_content[:1000],
            detailed_analysis=report_content,
        )

    def _prepare_analysis_prompt(self, topic: str, questions: List[Question]) -> str:
        return f"""
        Analyze the following research data about: {topic}
        
        Questions and Findings:
        {self._format_questions_and_findings(questions)}
        
        Provide a structured analysis covering:
         - Treat me as an expert in all subject matter.
        - Mistakes erode my trust, so be accurate and thorough.
        - Provide detailed explanations, I'm comfortable with lots of detail.
        - Value good arguments over authorities, the source is irrelevant.
        - Consider new technologies and contrarian ideas, not just the conventional wisdom.
        -look for Main themes and patterns
        -Conflicting information
        -Data gaps
        -Credibility of sources
        """

    def _format_questions_and_findings(self, questions: List[Question]) -> str:
        formatted = []
        for q in questions:
            findings = "\n".join([s.get("extracted_content", "") for s in q.sources])
            formatted.append(f"Question: {q.text}\nFindings: {findings}\n")
        return "\n".join(formatted)
