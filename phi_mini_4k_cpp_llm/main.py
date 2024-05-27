from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from llm import LLM_chat

app = FastAPI()
llm_model = LLM_chat()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/talk/")
async def chat(
    text: str = "",
    template: str = "You are a smart virtual assistant, please answer my question like a friend and briefly",
):
    if not text:
        return {"error": "text is required"}

    messages = [
        {
            "role": "system",
            "content": template,
        },
        {"role": "user", "content": text},
    ]

    return StreamingResponse(
        llm_model.generate_stream(messages), media_type="text/event-stream"
    )


@app.post("/chat/")
async def chat(
    messages: List[dict] = [
        {
            "role": "user",
            "content": "Can you provide ways to eat combinations of bananas and dragonfruits?",
        },
        {
            "role": "assistant",
            "content": "Sure! Here are some ways to eat bananas and dragonfruits together:",
        },
        {"role": "user", "content": "What about solving an 2x + 3 = 7 equation?"},
    ],
):
    if not messages:
        return {"error": "messages is required"}

    return StreamingResponse(
        llm_model.generate_stream(messages), media_type="text/event-stream"
    )
