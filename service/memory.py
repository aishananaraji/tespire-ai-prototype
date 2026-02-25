from typing import Dict, List


MEMORY_STORE: Dict[str, List[Dict]] = {}

def get_history(session_id: str):
    return MEMORY_STORE.get(session_id, [])

def save_turn(session_id: str, question: str, answer: str, intent: str):
    if session_id not in MEMORY_STORE:
        MEMORY_STORE[session_id] = []

    MEMORY_STORE[session_id].append({
        "question": question,
        "answer": answer,
        "intent": intent
    })

    
    MEMORY_STORE[session_id] = MEMORY_STORE[session_id][-3:]