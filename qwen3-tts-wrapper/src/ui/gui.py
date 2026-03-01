import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# ~/Documents/learning_projects/qwen3-tts-wrapper/gui.py

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import socket
import json
import subprocess
import os
#SK|
#TY|from config import SOCKET_PATH
#TX|
class TTSWidget(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="TTS 🎙️")
        self.set_default_size(160, 60)
        self.set_decorated(False)  # ללא frame — חלון מינימלי
       # self.set_keep_above(True)  # תמיד מעל
        self.set_hide_on_close(True)

        # כפתור toggle
        self.btn = Gtk.ToggleButton(label="⏸ כבוי")
        self.btn.connect("toggled", self.on_toggle)
        self.set_child(self.btn)

        # בדיקת סטטוס כל 2 שניות
        GLib.timeout_add(2000, self.check_status)

    def send_command(self, action):
        try:
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(SOCKET_PATH)
            client.send(json.dumps({"action": action}).encode())
            response = json.loads(client.recv(1024).decode())
            client.close()
            return response
        except Exception as e:
            print(f"שגיאת חיבור ל-daemon: {e}")
            return None

    def on_toggle(self, btn):
        if btn.get_active():
            btn.set_label("🎙️ מאזין...")
            self.send_command("start")
        else:
            btn.set_label("⏸ כבוי")
            self.send_command("stop")

    def check_status(self):
        response = self.send_command("status")
        if response:
            active = response.get("active", False)
            self.btn.set_active(active)
            self.btn.set_label("🎙️ מאזין..." if active else "⏸ כבוי")
        return True  # המשך ה-timer

class TTSApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="dev.razik.qwen3tts")

    def do_activate(self):
        win = TTSWidget(self)
        win.present()


if __name__ == "__main__":
    app = TTSApp()
    import sys
    sys.exit(app.run(sys.argv))

