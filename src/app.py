from llama_index.llms.openai_like import OpenAILike
from llama_index.core import Settings
import os

def get_llm():
    llm = OpenAILike(
        api_base="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),

        model="llama-3.1-8b-instant",

        is_chat_model=True,

        temperature=0.2,
        max_tokens=1024,
    )

    Settings.llm = llm
    Settings.context_window = 8192
    print("[DEBUG] LLM initialized successfully")

    return llm