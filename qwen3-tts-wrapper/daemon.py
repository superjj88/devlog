# ~/Documents/learning_projects/devlog/qwen3-tts-wrapper/daemon.py
import torch
import whisper
import gc
import socket
import threading
import json
import os
import subprocess
import numpy as np
import time
import soundfile as sf

MODEL_DIR = "/mnt/storage/models/qwen3-tts"
TTS_MODEL_PATH = f"{MODEL_DIR}/1.7B-CustomVoice"
SOCKET_PATH = "/tmp/qwen3tts.sock"
TEMP_PLAY_FILE = "/tmp/qwen_play.wav"

SILENCE_THRESHOLD = 0.02  # סף שמע (אפשר להקטין ל-0.01 אם זה לא קולט אותך מספיק טוב)
SILENCE_DURATION = 2.5    # כמה שניות של שקט מסמנות סוף משפט

class TTSDaemon:
    def __init__(self):
        self.tts_model = None
        self.stt_model = None
        self.is_active = False
        self.listen_thread = None

    def load_models(self):
        print("[TTS] טוען מודל Qwen-TTS...")
        from qwen_tts import Qwen3TTSModel
        
        self.tts_model = Qwen3TTSModel.from_pretrained(
            TTS_MODEL_PATH,
            device_map="cuda",
            dtype=torch.bfloat16,
        )
        print("[TTS] מודל TTS נטען ✅")
        
        print("[STT] טוען מודל Faster-Whisper Turbo...")
        from faster_whisper import WhisperModel
        # מודל טורבו שרץ על כרטיס המסך עם המרה מהירה של Float16
        self.stt_model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")
        print("[STT] מודל Faster-Whisper נטען ✅")


    def unload_models(self):
        print("[TTS] פורק מודלים...")
        self.is_active = False
        if self.tts_model: del self.tts_model
        if self.stt_model: del self.stt_model
        gc.collect()
        torch.cuda.empty_cache()

    def listen_until_silence(self):
        """קורא מהמיקרופון עם arecord ומנתח בזמן אמת ללא חסימה"""
        print("[TTS] 🎤 מאזין... (דבר עכשיו, אפסיק כשתשתוק ל-2.5 שניות)")
        
        # מפעילים arecord שיזרוק את המידע החוצה כזרם
        command = [
            "arecord", "-D", "hw:1,0", "-q", "-t", "raw", 
            "-f", "S16_LE", "-c", "1", "-r", "16000"
        ]
        
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"[TTS] שגיאת הפעלת arecord: {e}")
            return None

        frames = []
        silence_start = None
        has_spoken = False
        chunk_size = 4096  # קריאה של רבע שנייה בכל פעם

        try:
            while self.is_active:
                # ה-read של Python יכול להיתקע אם הקובץ אינסופי, אז משתמשים ב-os.read ישירות לביצוע בטוח
                raw_data = os.read(process.stdout.fileno(), chunk_size * 2)
                
                if not raw_data:
                    break
                
                # ממירים ל-float32 מנורמל עבור Whisper
                audio_chunk = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0
                volume = np.abs(audio_chunk).mean()
                
                frames.append(audio_chunk)

                if volume > SILENCE_THRESHOLD:
                    # זיהינו דיבור!
                    has_spoken = True
                    silence_start = None 
                elif has_spoken:
                    # שקט... האם עברו 2.5 שניות?
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > SILENCE_DURATION:
                        print("[TTS] ⏳ שתיקה זוהתה. עוצר הקלטה ומתחיל לעבד...")
                        break
        finally:
            # חייבים להרוג את arecord כדי לשחרר את המיקרופון לפעם הבאה
            process.kill()
            process.wait()

        if not has_spoken or len(frames) < 5:
            return None

        return np.concatenate(frames)


    def process_and_respond(self, audio_np):
        print("[STT] ⏳ מפענח דיבור...")
        start_time = time.time()
        
        # זיהוי ותרגום אופטימלי - אנחנו פוקדים עליו "לתרגם" לאנגלית
        # faster-whisper דורש קודם לנרמל את המערך ל-Float32
        segments, info = self.stt_model.transcribe(audio_np, task="translate")
        
        user_text = "".join([segment.text for segment in segments]).strip()
        lang = info.language
        
        end_time = time.time()
        
        if len(user_text) < 2: return
        print(f"[STT] 🗣️ זיהיתי ({lang}) תוך {end_time - start_time:.2f} שניות: {user_text}")

        # ממשיכים כרגיל לתשובה של Qwen...
        if lang == "he" or any("\u0590" <= c <= "\u05EA" for c in user_text):
            bot_reply = f"You said something in Hebrew, but I can only speak English right now."
        else:
            bot_reply = f"You said: {user_text}"

        print(f"[TTS] 🤖 עונה: {bot_reply}")

        audio_data, sample_rate = self.tts_model.generate_custom_voice(
            text=bot_reply,
            language="english",
            speaker="Vivian",
        )

        print("[TTS] 🔊 מנגן תשובה...")
        sf.write(TEMP_PLAY_FILE, audio_data[0], sample_rate, subtype='PCM_16')
        subprocess.run(["aplay", "-q", TEMP_PLAY_FILE], stderr=subprocess.DEVNULL)



    def listen_loop(self):
        while self.is_active:
            audio_np = self.listen_until_silence()
            if audio_np is not None:
                self.process_and_respond(audio_np)
            else:
                # מניעת לופ מהיר מדי אם הוא לא קלט כלום
                time.sleep(0.1)

    def start(self):
        if not self.is_active:
            self.load_models()
            self.is_active = True
            self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
            self.listen_thread.start()

    def stop(self):
        self.is_active = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        self.unload_models()

    def run_socket_server(self):
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(SOCKET_PATH)
        server.listen(1)
        print(f"[TTS] Daemon מאזין ב-{SOCKET_PATH}")
        while True:
            try:
                conn, _ = server.accept()
                data = conn.recv(1024).decode()
                if data:
                    cmd = json.loads(data)
                    if cmd["action"] == "start":
                        self.start()
                        conn.send(b'{"status": "started"}')
                    elif cmd["action"] == "stop":
                        self.stop()
                        conn.send(b'{"status": "stopped"}')
                    elif cmd["action"] == "status":
                        conn.send(json.dumps({"active": self.is_active}).encode())
                conn.close()
            except Exception:
                pass

if __name__ == "__main__":
    daemon = TTSDaemon()
    daemon.run_socket_server()
