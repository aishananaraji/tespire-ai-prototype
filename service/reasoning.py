#service/reasoning.py
def classify_intent(question: str):
    q = question.lower()

    if "enrollment" in q:
        return "enrollment"
    if "attendance" in q:
        return "attendance" 
    if "fee" in q or "payment" in q:
        return "fees"
    return "unknown"