import google.generativeai as genai
from typing import Dict, Any

class ContentAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def analyze_content(self, content: str, question: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze the following content in relation to this question: {question}
        
        Content:
        {content}
        
        Provide analysis in the following format:
        1. Relevance (0-10)
        2. Key findings
        3. Supporting evidence
        4. Potential biases or limitations
        """
        
        response = await self.model.generate_content_async(prompt)
        
        return {
            "analysis": response.text,
            "question": question,
            "raw_content": content
        } 