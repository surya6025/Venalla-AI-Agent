"""
VENALLA GOD-LEVEL AI AGENT - MAIN WINDOW
Complete multi-panel UI with auto-error handling
"""

import sys
import traceback
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTextEdit, QLineEdit, QPushButton, QLabel, QListWidget,
        QFileDialog, QMessageBox, QSplitter, QTabWidget, QStatusBar
    )
    from PyQt6.QtCore import Qt, QTimer
except Exception as e:
    print("PyQt6 import failed. Ensure PyQt6 is installed.")
    raise

# Minimal placeholder to avoid runtime errors if AgentCore is missing
try:
    from core.agent_core import AgentCore
except Exception:
    class AgentCore:
        def __init__(self):
            pass
        def process_command(self, command: str) -> str:
            return f"[AgentCore stub] Received: {command}"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Venalla God-Level AI Agent")
        self.resize(1200, 800)

        self.agent = AgentCore()

        container = QWidget()
        self.setCentralWidget(container)
        root_layout = QVBoxLayout(container)

        # Top status
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Auto-Recovery Enabled")

        # Splitter for left (tabs) and right (chat)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        root_layout.addWidget(splitter)

        # Left side tabs
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.tabs = QTabWidget()
        left_layout.addWidget(self.tabs)

        # File Explorer tab
        self.file_list = QListWidget()
        file_tab = QWidget()
        file_tab_layout = QVBoxLayout(file_tab)
        file_tab_layout.addWidget(QLabel("File Explorer"))
        file_tab_layout.addWidget(self.file_list)

        btn_row = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_open = QPushButton("Open")
        self.btn_attach = QPushButton("Attach")
        btn_row.addWidget(self.btn_refresh)
        btn_row.addWidget(self.btn_open)
        btn_row.addWidget(self.btn_attach)
        file_tab_layout.addLayout(btn_row)
        self.tabs.addTab(file_tab, "Files")

        # Plugin Manager tab (placeholder)
        plugin_tab = QWidget()
        plugin_layout = QVBoxLayout(plugin_tab)
        plugin_layout.addWidget(QLabel("Plugin Manager (Coming soon)"))
        self.tabs.addTab(plugin_tab, "Plugins")

        # Right side: Chat panel
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type a command or message…")
        self.send_button = QPushButton("Send")

        input_row = QHBoxLayout()
        input_row.addWidget(self.input_line)
        input_row.addWidget(self.send_button)

        right_layout.addWidget(QLabel("Chat"))
        right_layout.addWidget(self.chat_view, 1)
        right_layout.addLayout(input_row)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 800])

        # Signals
        self.send_button.clicked.connect(self.on_send)
        self.input_line.returnPressed.connect(self.on_send)
        self.btn_refresh.clicked.connect(self.refresh_files)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_attach.clicked.connect(self.attach_file)

        # Initial load
        self.refresh_files()

    def log(self, text: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_view.append(f"[{timestamp}] {text}")

    def on_send(self):
        text = self.input_line.text().strip()
        if not text:
            return
        self.log(f"You: {text}")
        self.input_line.clear()
        try:
            response = self.agent.process_command(text)
        except Exception as e:
            response = f"Error: {type(e).__name__}: {e}"
        self.log(f"Agent: {response}")

    def refresh_files(self):
        self.file_list.clear()
        try:
            cwd = Path.cwd()
            for p in cwd.iterdir():
                self.file_list.addItem(p.name)
            self.status_bar.showMessage("Files refreshed")
        except Exception as e:
            self.status_bar.showMessage(f"File load error: {e}")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", str(Path.cwd()))
        if not path:
            return
        try:
            content = Path(path).read_text(encoding='utf-8')
            self.log(f"Opened {path}\n{content[:1000]}{'...' if len(content)>1000 else ''}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file:\n{e}")

    def attach_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Attach File", str(Path.cwd()))
        if not path:
            return
        self.log(f"Attached file: {path}")

    def show_about(self):
        QMessageBox.about(
            self,
            "About Venalla",
            "Venalla God-Level AI Agent\nVersion 1.0.0\n\n"
            "Omnipotent desktop AI with auto-error rectification",
        )
