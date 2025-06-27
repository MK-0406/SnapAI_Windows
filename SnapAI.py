import sys
import os

log_file = os.path.expanduser("~/snapai_log.txt")
#sys.stdout = open(log_file, "a")
#sys.stderr = sys.stdout
print("\n\n--- SnapAI launched ---\n")

import hashlib
from PyQt5.QtCore import QBuffer
import time
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WATCHED_FOLDER = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
AI_MODEL = "llama3-70b-8192"

class FloatingPanel(QtWidgets.QWidget):
    updateTextSignal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.94)

        self.setStyleSheet("""
            QWidget {
                border-radius: 14px;
                background-color: rgba(20, 20, 20, 180);
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border-radius: 10px;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: rgba(200, 200, 200, 0.6);
                border-radius: 4px;
            }
        """)

        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)

        self.label = QtWidgets.QLabel("Welcome to SnapAI. Please wait for awhile after starting the monitoring for the app to load.")
        self.label.setStyleSheet("QLabel { color: white; font-size: 32px; padding: 14px; }")
        self.label.setWordWrap(True)

        self.content_layout.addWidget(self.label)
        self.scroll.setWidget(self.content_widget)
        layout.addWidget(self.scroll)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.start_btn = QtWidgets.QPushButton("Start")
        self.stop_btn = QtWidgets.QPushButton("Stop")
        self.quit_btn = QtWidgets.QPushButton("Quit")

        button_style = "QPushButton { color: white; font-size: 28px; padding: 6px 12px; }"
        self.start_btn.setStyleSheet(button_style)
        self.stop_btn.setStyleSheet(button_style)
        self.quit_btn.setStyleSheet(button_style)

        self.start_btn.clicked.connect(self.start_monitoring)
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.quit_btn.clicked.connect(QtWidgets.qApp.quit)

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.quit_btn)
        layout.addLayout(button_layout)

        self.resize(900, 500)
        self.move(400, 200)
        self.show()

        self.handler = ScreenshotHandler(self)
        self.observer = None
        self.monitoring = False
        self.updateTextSignal.connect(self.update_text)

        self.last_clipboard_hash = ""
        self.processing_clipboard = False
        self.clip_timer = QtCore.QTimer()
        self.clip_timer.timeout.connect(self.check_clipboard_image)
        self.clip_timer.start(1000)



    @QtCore.pyqtSlot(str)
    def update_text(self, new_text):
        self.label.setText(new_text)
        self.label.adjustSize()
        self.raise_()
        self.activateWindow()
        self.show()

    def start_monitoring(self):
        if self.monitoring:
            return
        self.observer = Observer()
        self.observer.schedule(self.handler, WATCHED_FOLDER, recursive=False)
        self.observer.start()
        self.update_text("Monitoring started...")
        self.monitoring = True

    def stop_monitoring(self):
        if self.observer and self.monitoring:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.update_text("Monitoring stopped.")
            self.monitoring = False

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def get_image_hash(self, image: QImage) -> str:
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        image.save(buffer, "PNG")
        return hashlib.md5(buffer.data()).hexdigest()

    def check_clipboard_image(self):
        if self.processing_clipboard:
            return

        clipboard = QtWidgets.QApplication.clipboard()
        mime = clipboard.mimeData()
        if mime.hasImage():
            image = clipboard.image()
            current_hash = self.get_image_hash(image)
            if current_hash != self.last_clipboard_hash:
                self.last_clipboard_hash = current_hash
                # Save to temporary file
                path = os.path.join(os.path.dirname(__file__), "clipboard_image.png")
                QPixmap.fromImage(image).save(path)
                def wrapped():
                    self.handler.process_screenshot(path)
                    self.processing_clipboard = False
                Thread(target=wrapped, daemon=True).start()

class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self, panel):
        self.panel = panel

    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith((".png", ".jpg", ".jpeg")):
            return
        Thread(target=self.process_screenshot, args=(event.src_path,), daemon=True).start()

    def process_screenshot(self, path):
        time.sleep(1)
        try:
            text = pytesseract.image_to_string(Image.open(path))
            print("🖼️ OCR Text:", text)
            if text.strip():
                ai_response = ask_ai(text)
                QtCore.QMetaObject.invokeMethod(
                    self.panel,
                    "update_text",
                    QtCore.Qt.QueuedConnection,
                    QtCore.Q_ARG(str, ai_response)
                )
        except Exception as e:
            print("Error:", e)
        finally:
            if "clipboard_image.png" in path:
                try:
                    os.remove(path)
                except Exception:
                    pass

def ask_ai(prompt):
    import datetime
    with open(log_file, "a") as f:
        f.write(f"\n[{datetime.datetime.now()}] Sending prompt to AI: {prompt}\n")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": AI_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        with open(log_file, "a") as f:
            f.write(f"[{datetime.datetime.now()}] Status: {response.status_code}\n")
            f.write(f"Response text: {response.text[:500]}\n")
        if response.status_code != 200:
            print("API Error:", response.status_code, response.text)
            return f"Error {response.status_code}: {response.text}"
        result = response.json()['choices'][0]['message']['content']
        print("AI Response:", result)
        return result
    except Exception as e:
        print("AI Exception:", e)
        with open(log_file, "a") as f:
            f.write(f"[{datetime.datetime.now()}] Exception: {e}\n")
        return f"Error: {e}"

def main():
    app = QtWidgets.QApplication(sys.argv)
    panel = FloatingPanel()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
