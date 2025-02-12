from openai import AsyncOpenAI
from typing import List
from models.schemas import Question


class QuestionGenerator:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_initial_questions(
        self, topic: str, max_questions: int = 5
    ) -> List[Question]:
        prompt = f"""
        Generate {max_questions} essential research questions about: {topic}
        Focus on questions that:
        1. Address fundamental aspects of the topic
        2. Challenge common assumptions
        3. Explore causal relationships
        4. Investigate historical context
        """

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        questions = response.choices[0].message.content.strip().split("\n")
        return [Question(text=q.strip()) for q in questions if q.strip()]

    async def generate_sub_questions(
        self, question: Question, depth: int = 1
    ) -> Question:
        if depth <= 0:
            return question

        prompt = f"Generate 3 follow-up questions for: {question.text}"
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        sub_questions = [
            Question(text=q.strip())
            for q in response.choices[0].message.content.strip().split("\n")
        ]

        question.sub_questions = sub_questions

        for sub_q in question.sub_questions:
            await self.generate_sub_questions(sub_q, depth - 1)

        return question
