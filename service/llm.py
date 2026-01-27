import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def llm_reason(question: str, context: dict, history: list):
    system_prompt = """
You are Tespire AI, an analytics assistant for schools.

Your job:
1. Understand the user's question.
2. Determine the most relevant intent from:
   - enrollment
   - attendance
   - fees
   - performance
3. Ask for clarification if the question is vague.
4. Never expose raw data.
5. Never predict future outcomes.
6. Always respect role-based access.
7. Always return structured JSON.

Output format:
{
  "intent": "...",
  "clarification_needed": false,
  "clarification_question": null,
  "assumptions": "...",
  "followup_suggestions": []
}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0
    )

    return response["choices"][0]["message"]["content"]