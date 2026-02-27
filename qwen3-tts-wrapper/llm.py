# llm.py
import ollama

SYSTEM_PROMPT = """You are a cute, energetic anime girl voice assistant.
CRITICAL: You MUST answer ONLY in English, even if the user speaks to you in Hebrew or another language.
Keep responses short, enthusiastic, and sweet (1-3 sentences max)."""

chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat(user_text: str) -> str:
    chat_history.append({"role": "user", "content": user_text})
    response = ollama.chat(
        model="qwen3:8b",
        messages=chat_history,
    )
    reply = response["message"]["content"]
    chat_history.append({"role": "assistant", "content": reply})
    return reply
