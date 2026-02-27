# stt.py
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cuda", compute_type="float16")

# stt.py

# ... (הקוד שלמעלה עם ה-import וה-WhisperModel נשאר אותו דבר) ...

def record_until_silence(samplerate=16000, silence_threshold=0.015, silence_duration=2.5, min_recording_duration=0.5):
    """
    מקליט אודיו ומפסיק כשיש שתיקה ממושכת.
    - silence_threshold: הורדנו מעט (ל-0.015) כדי שלא יחשוב שמילים חלשות הן "שקט".
    - silence_duration: הועלה ל-2.5 שניות, כדי לתת לך זמן לקחת אוויר או לחשוב באמצע המשפט.
    - min_recording_duration: מחייב לפחות חצי שנייה של דיבור.
    """
    chunk_size = int(samplerate * 0.1)  # רסיסים של 100ms
    audio_chunks = []
    silent_chunks = 0
    required_silent = int(silence_duration / 0.1)
    
    is_speaking = False

    with sd.InputStream(samplerate=samplerate, channels=1, dtype='float32') as stream:
        print("🎤 מחכה לדיבור...")
        while True:
            chunk, _ = stream.read(chunk_size)
            rms = np.sqrt(np.mean(chunk**2))
            
            # אם יש קול שחזק מהסף
            if rms > silence_threshold:
                if not is_speaking:
                    print("🗣️ מזהה דיבור, מקליט...")
                is_speaking = True
                silent_chunks = 0  # מאפס את מונה השתיקה כי דיברת
            else:
                # אם אנחנו כבר בתוך הקלטה, נתחיל לספור את השתיקה
                if is_speaking:
                    silent_chunks += 1
                
            if is_speaking:
                audio_chunks.append(chunk)
                
            # תנאי עצירה: דיברנו, ועכשיו שתקנו למשך silence_duration שלם (2.5 שניות עכשיו)
            if is_speaking and silent_chunks >= required_silent:
                print("⏳ ההקלטה הסתיימה (שתיקה ארוכה מדי). מעבד...")
                break

    # בדיקה האם ההקלטה קצרה מדי
    total_duration = (len(audio_chunks) - silent_chunks) * 0.1 # זמן נטו בלי שתיקת הסוף
    if total_duration < min_recording_duration:
        return None  # קצר מדי

    audio = np.concatenate(audio_chunks).flatten()
    return audio

# ... (שאר הפונקציה transcribe נשארת אותו דבר) ...


def transcribe(audio: np.ndarray, language="he") -> str:
    # prompt ראשוני מונע הרבה מבעיות ה"הזיה" של מילים ריקות כמו Thank you
    segments, _ = model.transcribe(
        audio, 
        language=language, 
        beam_size=5,
        condition_on_previous_text=False, # מונע חזרה על משפטים קודמים
        vad_filter=True, # מפעיל מסנן קול מובנה של Whisper שמתעלם מרעשים
        vad_parameters=dict(min_silence_duration_ms=500)
    )
    
    text = " ".join(s.text for s in segments).strip()
    return text
