#!/bin/bash
# ~/Documents/learning_projects/qwen3-tts-wrapper/start.sh

# נתיב הפרויקט
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# מנקים תהליכים ישנים כדי לא למלא את ה-VRAM
pkill -f "python.*daemon.py"
pkill -f "python.*gui.py"

# הפעלת סביבה וירטואלית
source .venv/bin/activate

# 1. הפעלת ה-Daemon ברקע לחלוטין
python daemon.py > /tmp/qwen3tts_daemon.log 2>&1 &
DAEMON_PID=$!

echo "🎙️ ה-Daemon רץ ברקע (PID: $DAEMON_PID). מעלה ממשק..."
sleep 1

# 2. הפעלת ה-GUI כרגיל (הוא זה שיחזיק את הטרמינל, וכשתסגור את החלון הוא ישתחרר)
python gui.py

# 3. ברגע שסגרת את חלון ה-GUI (או עשית Ctrl+C), נהרוג גם את ה-daemon
echo "מכבה את המערכת ומנקה VRAM..."
kill $DAEMON_PID
pkill -f "python.*daemon.py"

