from fastapi import APIRouter, Query

from movieapi.constants import BASE_URL

router = APIRouter(prefix=BASE_URL)


@router.post("/llm/chat", summary="Mock LLM conversational endpoint")
def chat(q: str = Query(..., description="User's question or prompt")):
    answer = (
        f"You asked: '{q}'. Here's a quick thought — "
        "I’d approach that step by step, focusing on clarity and key details. "
        "Would you like me to expand on that?"
    )

    return {"model": "mock-llm", "answer": answer}
