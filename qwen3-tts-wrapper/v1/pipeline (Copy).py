import time
import numpy as np
import sounddevice as sd
import torch
from stt import record_until_silence, transcribe
from llm import chat

# --- Qwen3-TTS Setup ---
print("⏳ Loading Qwen3-TTS model...")
from qwen_tts import Qwen3TTSModel
import torch
import sounddevice as sd

# משתמשים במודל CustomVoice כפי שבחרת
tts_model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice", 
    device_map="cuda", 
    dtype=torch.float16
)
print("✅ Qwen3-TTS Model loaded.")

def speak(text, language="English"):
    if not text: return
    print(f"🔊 Generating audio for: '{text}'...")
    
    try:
        wavs, sr = tts_model.generate_custom_voice(
            text=text,
            language=language, # אנחנו מגדירים את השפה לאנגלית
            speaker="Ono_anna", # קול יפני נשי בסיסי שידבר באנגלית עם המבטא/גוון הנכון
            instruct="A very cute, energetic, and sweet young anime girl voice, speaking enthusiastically with high pitch.", # ההוראה שמעצבת את הקול
            max_new_tokens=2048
        )
        
        audio_data = wavs[0]
        sd.play(audio_data, samplerate=sr)
        sd.wait()
        
    except Exception as e:
        print(f"❌ Error in TTS: {e}")

# --- Main Loop ---

# בתוך pipeline.py, הלולאה תיראה כך:
def voice_loop():
    print("🔊 Voice assistant ready. Ctrl+C to stop.")
    
    while True:
        try:
            # 1. הקלטה
            audio = record_until_silence()
            if audio is None:
                continue

            # 2. המרה לטקסט (Whisper)
            user_text = transcribe(audio, language=None)
            
            # --- סינון "הזיות" ורעשים קצרים ---
            if not user_text:
                continue
                
            user_text = user_text.strip()
            
            # רשימה של הזיות נפוצות ש-Whisper ממציא כשיש שקט
            hallucinations = ["thank you.", "thank you", "thanks.", "subscribe", ".", "am", "is", "a", "the"]
            
            # אם הטקסט קצר מדי (פחות מ-2 תווים) או נמצא ברשימת ההזיות
            if len(user_text) < 2 or user_text.lower() in hallucinations:
                print(f"👻 התעלם מרעש/הזיה: {user_text}")
                continue
            # ----------------------------------

            print(f"👤 {user_text}")


            # 3. קבלת תשובה (Ollama יענה תמיד באנגלית בזכות הפרומפט החדש)
            reply = chat(user_text)
            print(f"🤖 {reply}")

            # 4. המרה לדיבור (TTS - תמיד שולחים לאנגלית)
            speak(reply, language="English")
            
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n👋 Stopping...")
            break
        except Exception as e:
            print(f"\n❌ Error in loop: {e}")
            time.sleep(1)

if __name__ == "__main__":
    voice_loop()
