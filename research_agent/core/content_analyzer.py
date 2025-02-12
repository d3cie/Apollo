import google.generativeai as genai
from typing import Dict, Any

class ContentAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def analyze_content(self, content: str, question: str) -> Dict[str, Any]:
        # Limit content length
        content = content[:1000]  # Only analyze first 1000 chars
        
        prompt = f"""
        Analyze this content briefly for the question: {question}
        Content: {content}
        
        Provide a BRIEF analysis with:
        1. Relevance (0-10)
        2. Key finding (1-2 sentences)
        3. Main evidence (1 sentence)
        
        Keep the total response under 100 words.
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            return {
                "analysis": response.text,
                "question": question,
                "content_length": len(content)
            }
        except Exception as e:
            print(f"Analysis error: {str(e)}")
            return {
                "analysis": "Analysis failed",
                "question": question,
                "error": str(e)
            } 