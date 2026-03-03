import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QTextEdit, QLineEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QImage, QFont

from .screen_capture import ScreenCapture
from .audio_recorder import AudioRecorder
from .agent_api import AgentAPI
from .executor import ActionExecutor
from .utils import pil_to_b64_png


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI Navigator PRO (Gemini)")
        self.resize(1200, 720)

        self.capture = ScreenCapture(monitor_index=1)
        self.audio = AudioRecorder()
        self.api = AgentAPI(os.getenv("AGENT_URL", "http://127.0.0.1:8080"))
        self.exec = ActionExecutor()

        # left: screen preview
        self.preview = QLabel("Screen preview...")
        self.preview.setFixedSize(640, 400)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setStyleSheet("background:#111; border-radius:12px;")

        self.btn_snap = QPushButton("📸 Screenshot olish")
        self.btn_snap.clicked.connect(self.do_snapshot)

        self.chk_voice = QCheckBox("🎙 Ovozni ham yubor (2.5s)")
        self.chk_voice.setChecked(False)

        # right: intent + plan + execute
        self.intent = QLineEdit()
        self.intent.setPlaceholderText("Masalan: 'Chrome’da youtube studio ochib kommentlarni o‘chir'")

        self.btn_plan = QPushButton("🧠 Reja tuz (Plan)")
        self.btn_plan.clicked.connect(self.do_plan)

        self.btn_exec = QPushButton("⚡ Rejani bajar (Execute)")
        self.btn_exec.clicked.connect(self.do_execute)
        self.btn_exec.setEnabled(False)

        self.chk_confirm = QCheckBox("Har safar execute oldidan tasdiq so‘ra")
        self.chk_confirm.setChecked(True)

        self.status = QLabel("🟡 Ready")
        self.status.setStyleSheet("color:#4aa3ff;")
        self.status.setFont(QFont("Arial", 11))

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("background:#0b0f14; color:#e6f1ff; border-radius:12px; padding:10px;")

        # layout
        left = QVBoxLayout()
        left.addWidget(self.preview)
        left.addWidget(self.btn_snap)
        left.addWidget(self.chk_voice)
        left.addStretch(1)

        right = QVBoxLayout()
        right.addWidget(self.status)
        right.addWidget(QLabel("🎯 Maqsad (intent):"))
        right.addWidget(self.intent)

        btnrow = QHBoxLayout()
        btnrow.addWidget(self.btn_plan)
        btnrow.addWidget(self.btn_exec)
        right.addLayout(btnrow)

        right.addWidget(self.chk_confirm)
        right.addWidget(QLabel("🧾 Plan / Log:"))
        right.addWidget(self.log)

        root = QHBoxLayout()
        root.addLayout(left, 0)
        root.addLayout(right, 1)
        self.setLayout(root)

        self.last_img = None
        self.last_plan = None

        # auto-refresh preview every 1s
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_preview)
        self.timer.start(1000)

    def append(self, text: str):
        self.log.append(text)

    def set_status(self, s: str):
        self.status.setText(s)

    def refresh_preview(self):
        try:
            img = self.capture.grab()
            self.last_img = img
            self._set_preview(img)
        except Exception as e:
            self.set_status(f"❌ Screen capture xato: {e}")

    def _set_preview(self, pil_img):
        rgb = pil_img.convert("RGB")
        w, h = rgb.size
        data = rgb.tobytes("raw", "RGB")
        qimg = QImage(data, w, h, QImage.Format.Format_RGB888)
        pix = QPixmap.fromImage(qimg).scaled(
            self.preview.width(),
            self.preview.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.preview.setPixmap(pix)

    def do_snapshot(self):
        self.refresh_preview()
        self.append("📸 Screenshot yangilandi.")

    def do_plan(self):
        if self.last_img is None:
            self.refresh_preview()
        if self.last_img is None:
            QMessageBox.warning(self, "Xato", "Screenshot olinmadi.")
            return

        intent = self.intent.text().strip()
        if not intent:
            QMessageBox.warning(self, "Xato", "Intent kiriting.")
            return

        self.set_status("🧠 Plan tuzilmoqda...")
        self.btn_plan.setEnabled(False)
        self.btn_exec.setEnabled(False)

        try:
            w, h = self.last_img.size
            payload = {
                "intent": intent,
                "screenshot_b64": pil_to_b64_png(self.last_img),
                "screenshot_width": w,
                "screenshot_height": h,
            }

            if self.chk_voice.isChecked():
                self.append("🎙 Audio yozilyapti (2.5s)...")
                payload["audio_wav_b64"] = self.audio.record_wav_b64(2.5)

            plan = self.api.plan(payload)
            self.last_plan = plan

            self.append("✅ PLAN OK")
            self.append(f"Goal: {plan.get('goal')}")
            self.append(f"Confidence: {plan.get('confidence')}")
            self.append("Actions:")
            for i, a in enumerate(plan.get("actions", []), 1):
                self.append(f"{i}. {a.get('type')}  {a}  // {a.get('reason','')}")
            notes = plan.get("notes", "")
            if notes:
                self.append(f"Notes: {notes}")

            self.btn_exec.setEnabled(True)
            self.set_status("✅ Plan tayyor. Execute mumkin.")
        except Exception as e:
            self.set_status(f"❌ Plan xato: {e}")
            self.append(f"ERROR: {e}")
        finally:
            self.btn_plan.setEnabled(True)

    def do_execute(self):
        if not self.last_plan:
            return
        actions = self.last_plan.get("actions", [])
        if not actions:
            QMessageBox.warning(self, "Xato", "Actions bo‘sh.")
            return

        if self.chk_confirm.isChecked():
            ok = QMessageBox.question(
                self,
                "Tasdiq",
                "Rejani bajarishni xohlaysizmi?\n(FAILSAFE: sichqonni yuqori chap burchakka olib boring to‘xtatish uchun)"
            )
            if ok != QMessageBox.StandardButton.Yes:
                return

        self.set_status("⚡ Execute boshlandi...")
        self.append("⚡ EXECUTING...")
        try:
            self.exec.execute(actions)
            self.set_status("✅ Execute tugadi.")
            self.append("✅ DONE")
        except Exception as e:
            self.set_status(f"❌ Execute xato: {e}")
            self.append(f"ERROR: {e}")