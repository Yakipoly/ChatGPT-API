# -*- coding: utf-8 -*-
import openai, uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

openai.api_key = "sk-_"

OPENAI_COMPLETION_OPTIONS = {
    "temperature": 0.7,
    "max_tokens": 4000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


class Message(BaseModel):
    text: str
    model: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chatgpt/send_one_message")
async def get_one_message(data: Message):
    try:
        r = openai.ChatCompletion.create(
            model=data.model,
            messages=[{"role": "user", "content": data.text}],
            **OPENAI_COMPLETION_OPTIONS,
        )
        return {"result": r.choices[0].message["content"]}
    except openai.error.APIError as e:
        return {
            "result": None,
            "error_message": str(e),
        }


uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=3, reload=False)
