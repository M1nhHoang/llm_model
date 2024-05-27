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
    template: str = "Bạn là một trợ lý ảo thông minh, hãy trả lời câu hỏi của tôi tất cả nhưng gì bạn biết như một người bạn và ngắn gọn nhé",
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
            "role": "system",
            "content": "Bạn là một trợ lý ảo thông minh, hãy trả lời câu hỏi của tôi tất cả nhưng gì bạn biết như một người bạn và ngắn gọn nhé",
        },
        {
            "role": "user",
            "content": "Bạn có thể cung cấp cách ăn kết hợp chuối và thanh long được không?",
        },
        {
            "role": "assistant",
            "content": "Chắc chắn! Dưới đây là một số cách ăn chuối và thanh long cùng nhau:",
        },
        {"role": "user", "content": "Còn việc giải phương trình 2x + 3 = 7 thì sao?"},
    ],
):
    if not messages:
        return {"error": "messages is required"}

    return StreamingResponse(
        llm_model.generate_stream(messages), media_type="text/event-stream"
    )
