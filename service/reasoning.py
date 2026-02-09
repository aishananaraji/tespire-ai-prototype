import requests

HF_URL = "https://tespire-ai.hf.space/run/predict"

def llm_reason(question, context, history):
    prompt = f"""
You are an AI for school analytics.

Conversation history:
{history}

User role: {context['role']}
Question: {question}

Classify the user's intent as one of:
- enrollment
- attendance
- fees
- performance
- unknown
"""

    try:
        response = requests.post(
            HF_URL,
            json={"data": [prompt]},
            timeout=20
        )
        result = response.json()
        return result["data"][0].strip().lower()

    except Exception as e:
        print("HF error:", e)
        return "unknown"
