from openai import AsyncOpenAI
from typing import List
from models.schemas import Question
from datetime import date


class QuestionGenerator:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_initial_questions(
        self, topic: str, max_questions: int = 5
    ) -> List[Question]:
        prompt = f"""
        Generate {max_questions} essential research questions about: {topic}
        Focus on questions that:
       ou are an expert researcher. Today is ${date.today()}. Follow these instructions when responding:
        - You may be asked to research subjects that is after your knowledge cutoff, assume the user is right when presented with news.
        - The user is a highly experienced analyst, no need to simplify it, be as detailed as possible and make sure your response is correct.
        - Be highly organized.
        - Suggest solutions that I didn't think about.
        - Be proactive and anticipate my needs.
        - You may use high levels of speculation or prediction, just flag it for me.`;
        -if its a casual topic adjust accordingly, for things such as current events and sports generate google search query like for most infomrtive best results and thegossip 
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
            model="gpt-4o",
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
