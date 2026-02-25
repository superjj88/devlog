#!/usr/bin/env python3
import subprocess, sys, os
from datetime import date
from pathlib import Path
import tomllib, httpx

BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

with open(BASE_DIR / "config.toml", "rb") as f:
    CONFIG = tomllib.load(f)

TODAY = date.today().isoformat()
LOG_FILE = LOGS_DIR / f"{TODAY}.md"

TEMPLATE = f"""# {TODAY} — Dev Log

## ✅ מה עשיתי היום
- 

## 🧱 מה חסם אותי
- 

## 💡 מה למדתי
- 

## 🎯 מחר
- 
"""

def cmd_new():
    if not LOG_FILE.exists():
        LOG_FILE.write_text(TEMPLATE)
    subprocess.run(["nvim", str(LOG_FILE)])

def cmd_summarize():
    if not LOG_FILE.exists():
        print("אין לוג להיום. הרץ תחילה: devlog new")
        sys.exit(1)

    content = LOG_FILE.read_text()
    prompt = f"אתה עוזר DevOps. קרא את יומן העבודה הזה וספק:\n1. 3 נקודות חוזק שראית\n2. 3 דברים לשפר\n3. מטרה אחת ברורה למחר\n\n---\n{content}"

    response = httpx.post(
        "http://localhost:11434/api/generate",
        json={"model": CONFIG["ollama"]["model"], "prompt": prompt, "stream": False},
        timeout=120
    )
    print("\n🤖 Ollama Summary:\n")
    print(response.json()["response"])

def cmd_commit():
    msg = f"devlog: {TODAY}"
    subprocess.run(["git", "-C", str(BASE_DIR), "add", "."])
    subprocess.run(["git", "-C", str(BASE_DIR), "commit", "-m", msg])
    subprocess.run(["git", "-C", str(BASE_DIR), "push"])
    print(f"✅ Committed: {msg}")

COMMANDS = {"new": cmd_new, "summarize": cmd_summarize, "commit": cmd_commit}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "new"
    COMMANDS.get(cmd, lambda: print(f"פקודה לא מוכרת: {cmd}"))()

