"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         CYBER PLANNER v2.0                                   ║
║                    Advanced Task Management System                            ║
║                                                                              ║
║  Made by: galmx (xdrew87)                                                   ║
║  GitHub: https://github.com/xdrew87/cyber-planner                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

FEATURES:
  ✓ Full calendar with month navigation
  ✓ Task creation with title, time, duration, category, and notes
  ✓ Edit & duplicate tasks via right-click context menu
  ✓ Search & filter tasks by title or notes
  ✓ Sort tasks by time, duration, or category
  ✓ Keyboard shortcuts: N (new task), Del (delete selected)
  ✓ Drag-and-drop tasks between dates
  ✓ Task reminders (15min, 5min, at time)
  ✓ Discord webhook notifications
  ✓ System tray integration with notifications
  ✓ Weekly analytics with task count & time breakdown
  ✓ CSV export/import for backup and data migration
  ✓ Custom categories (editable in settings)
  ✓ Today's agenda popup on startup
  ✓ Dark theme with cyberpunk aesthetic
  ✓ Custom background image/GIF support
  ✓ Persistent storage (JSON-based)
  ✓ Priority levels (Low, Medium, High)
  ✓ Recurring tasks (Daily, Weekly, Monthly)
  ✓ Pomodoro timer (25-minute sessions)
  ✓ Quick actions (Snooze, Pomodoro)

KEYBOARD SHORTCUTS:
  N - Create new task
  Del - Delete selected task

USAGE:
  Right-click any task to edit, duplicate, or delete
  Use search bar to filter tasks by title or notes
  Set categories for organization and time tracking
  Export/import CSV for data portability

LICENSE: Custom License - All rights reserved.
For terms and conditions, see LICENSE file.
"""

import sys
import os
import json
import uuid
import calendar
from datetime import datetime, timedelta, date

import requests
from PyQt6.QtCore import Qt, QMimeData, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QDrag, QIcon, QColor, QPalette, QMovie, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QDialog,
    QLineEdit,
    QComboBox,
    QTimeEdit,
    QSpinBox,
    QMessageBox,
    QFormLayout,
    QDialogButtonBox,
    QSplitter,
    QGroupBox,
    QSystemTrayIcon,
    QMenu,
    QFileDialog,
    QTextEdit,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

APP_NAME = "Cyber Planner"
TASKS_FILE = "tasks.json"
SETTINGS_FILE = "settings.json"
ICON_FILE = "cyber_planner.ico"

CATEGORY_COLORS = {
    "Work": "#3B82F6",
    "Personal": "#10B981",
    "Urgent": "#EF4444",
    "Coding": "#8B5CF6",
    "Health": "#F59E0B",
    "Finance": "#06B6D4",
    "Learning": "#EC4899",
    "Other": "#6B7280",
}

CATEGORY_BG = {
    "Work": "#0F2447",
    "Personal": "#0D3329",
    "Urgent": "#3A1111",
    "Coding": "#24104A",
    "Health": "#332D1B",
    "Finance": "#0D3A42",
    "Learning": "#42132E",
    "Other": "#222630",
}

REMINDER_OFFSETS_MINUTES = [15, 5, 0]

PRIORITY_COLORS = {
    "Low": "#10B981",
    "Medium": "#F59E0B",
    "High": "#EF4444",
}

BACKGROUND_FILE = "background.pgn"   # can also be .gif
BACKGROUND_OPACITY = 0.18           # transparency so UI stays readable


def resource_path(relative_path: str) -> str:
    """
    Return the correct absolute path for local runs and PyInstaller builds.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def ensure_file(path: str, default_data):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)


def load_json(path: str, default_data):
    ensure_file(path, default_data)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_data


def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def date_key(dt: date) -> str:
    return dt.strftime("%Y-%m-%d")


def parse_date_key(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def combine_date_time(date_str: str, hhmm: str) -> datetime:
    dt_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    dt_time = datetime.strptime(hhmm, "%H:%M").time()
    return datetime.combine(dt_date, dt_time)


def pretty_hours(minutes: int) -> str:
    hours = minutes / 60
    return f"{hours:.1f}h"


class Storage:
    def __init__(self):
        self.tasks = load_json(TASKS_FILE, {})
        self.settings = load_json(
            SETTINGS_FILE,
            {
                "discord_webhook_url": "",
                "reminders_enabled": True,
                "tray_notifications_enabled": True,
                "background_file": "",
                "custom_categories": ["Work", "Personal", "Urgent", "Coding"],
            },
        )

    def save_tasks(self):
        save_json(TASKS_FILE, self.tasks)

    def save_settings(self):
        save_json(SETTINGS_FILE, self.settings)

    def get_tasks_for_date(self, date_str: str):
        return self.tasks.get(date_str, [])

    def add_task(self, date_str: str, task: dict):
        self.tasks.setdefault(date_str, []).append(task)
        self.tasks[date_str].sort(key=lambda x: x["time"])
        self.save_tasks()

    def delete_task(self, date_str: str, task_id: str):
        if date_str not in self.tasks:
            return
        self.tasks[date_str] = [t for t in self.tasks[date_str] if t["id"] != task_id]
        if not self.tasks[date_str]:
            del self.tasks[date_str]
        self.save_tasks()

    def move_task(self, source_date: str, target_date: str, task_id: str):
        if source_date not in self.tasks:
            return False

        task = None
        remaining = []
        for t in self.tasks[source_date]:
            if t["id"] == task_id and task is None:
                task = t
            else:
                remaining.append(t)

        if task is None:
            return False

        self.tasks[source_date] = remaining
        if not self.tasks[source_date]:
            del self.tasks[source_date]

        task["reminders_sent"] = []
        self.tasks.setdefault(target_date, []).append(task)
        self.tasks[target_date].sort(key=lambda x: x["time"])
        self.save_tasks()
        return True

    def update_task(self, date_str: str, updated_task: dict):
        if date_str not in self.tasks:
            return
        for i, t in enumerate(self.tasks[date_str]):
            if t["id"] == updated_task["id"]:
                self.tasks[date_str][i] = updated_task
                break
        self.tasks[date_str].sort(key=lambda x: x["time"])
        self.save_tasks()


class AddTaskDialog(QDialog):
    def __init__(self, parent=None, selected_date: str = "", task: dict = None, categories: list = None):
        super().__init__(parent)
        self.task = task
        self.setWindowTitle("Edit Task" if task else "Add Task")
        self.setModal(True)
        self.resize(500, 450)
        self.selected_date = selected_date
        self.categories = categories or ["Work", "Personal", "Urgent", "Coding"]

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Fix website #1 backend")
        if task:
            self.title_input.setText(task.get("title", ""))

        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")
        if task:
            self.time_input.setText(task.get("time", ""))
        else:
            self.time_input.setTime(datetime.now().time().replace(second=0, microsecond=0))

        # Duration with unit selector
        duration_layout = QHBoxLayout()
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 999)
        self.duration_unit = QComboBox()
        self.duration_unit.addItems(["Minutes", "Hours", "Days"])
        
        # Set initial duration and unit based on task
        if task:
            minutes = task.get("duration_minutes", 60)
            if minutes >= 1440:  # >= 1 day
                days = minutes // 1440
                self.duration_input.setValue(days if days > 0 else 1)
                self.duration_unit.setCurrentText("Days")
            elif minutes >= 60:  # >= 1 hour
                hours = minutes // 60
                self.duration_input.setValue(hours if hours > 0 else 1)
                self.duration_unit.setCurrentText("Hours")
            else:
                self.duration_input.setValue(minutes)
                self.duration_unit.setCurrentText("Minutes")
        else:
            self.duration_input.setValue(1)
            self.duration_unit.setCurrentText("Hours")
        
        duration_layout.addWidget(self.duration_input)
        duration_layout.addWidget(self.duration_unit)

        self.category_input = QComboBox()
        self.category_input.addItems(self.categories)
        if task:
            self.category_input.setCurrentText(task.get("category", self.categories[0]))

        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        if task:
            self.priority_input.setCurrentText(task.get("priority", "Medium"))
        else:
            self.priority_input.setCurrentText("Medium")

        self.recurring_input = QComboBox()
        self.recurring_input.addItems(["None", "Daily", "Weekly", "Monthly"])
        if task:
            self.recurring_input.setCurrentText(task.get("recurring", "None"))
        else:
            self.recurring_input.setCurrentText("None")

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add notes or description...")
        self.notes_input.setMaximumHeight(100)
        if task:
            self.notes_input.setPlainText(task.get("notes", ""))

        form.addRow("Task Title", self.title_input)
        form.addRow("Time", self.time_input)
        form.addRow("Duration", duration_layout)
        form.addRow("Category", self.category_input)
        form.addRow("Priority", self.priority_input)
        form.addRow("Recurring", self.recurring_input)
        form.addRow("Notes", self.notes_input)
        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Missing Task", "Please enter a task title.")
            return
        self.accept()

    def get_task(self):
        # Convert duration to minutes based on selected unit
        duration_value = self.duration_input.value()
        duration_unit = self.duration_unit.currentText()
        
        if duration_unit == "Hours":
            duration_minutes = duration_value * 60
        elif duration_unit == "Days":
            duration_minutes = duration_value * 1440
        else:  # Minutes
            duration_minutes = duration_value
        
        task_data = {
            "id": self.task["id"] if self.task else str(uuid.uuid4()),
            "title": self.title_input.text().strip(),
            "time": self.time_input.time().toString("HH:mm"),
            "duration_minutes": duration_minutes,
            "category": self.category_input.currentText(),
            "priority": self.priority_input.currentText(),
            "recurring": self.recurring_input.currentText(),
            "notes": self.notes_input.toPlainText().strip(),
            "created_at": self.task.get("created_at", datetime.now().isoformat()) if self.task else datetime.now().isoformat(),
            "reminders_sent": self.task.get("reminders_sent", []) if self.task else [],
        }
        return task_data


class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None, storage=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(500, 400)
        self.settings = settings or {}
        self.storage = storage
        self.categories = settings.get("custom_categories", []) if settings else []

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.webhook_input = QLineEdit()
        self.webhook_input.setText(self.settings.get("discord_webhook_url", ""))
        self.webhook_input.setPlaceholderText("Discord webhook URL")

        self.reminders_combo = QComboBox()
        self.reminders_combo.addItems(["Enabled", "Disabled"])
        self.reminders_combo.setCurrentText(
            "Enabled" if self.settings.get("reminders_enabled", True) else "Disabled"
        )

        self.tray_combo = QComboBox()
        self.tray_combo.addItems(["Enabled", "Disabled"])
        self.tray_combo.setCurrentText(
            "Enabled" if self.settings.get("tray_notifications_enabled", True) else "Disabled"
        )

        form.addRow("Discord Webhook", self.webhook_input)
        form.addRow("Reminders", self.reminders_combo)
        form.addRow("Tray Notifications", self.tray_combo)
        layout.addLayout(form)

        note = QLabel(
            "Security note: for production use, set DISCORD_WEBHOOK_URL as an environment variable.\n"
            "If that env var exists, it overrides the saved setting."
        )
        note.setWordWrap(True)
        layout.addWidget(note)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_settings(self):
        return {
            "discord_webhook_url": self.webhook_input.text().strip(),
            "reminders_enabled": self.reminders_combo.currentText() == "Enabled",
            "tray_notifications_enabled": self.tray_combo.currentText() == "Enabled",
        }


class DraggableTaskList(QListWidget):
    def __init__(self, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setAlternatingRowColors(False)
        self.setSpacing(6)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        item = self.itemAt(position)
        if not item:
            return

        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        duplicate_action = menu.addAction("Duplicate")
        menu.addSeparator()
        delete_action = menu.addAction("Delete")

        action = menu.exec(self.mapToGlobal(position))
        if self.main_window:
            if action == edit_action:
                self.main_window.edit_task(item)
            elif action == duplicate_action:
                self.main_window.duplicate_task(item)
            elif action == delete_action:
                self.main_window.delete_task_from_menu(item)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item is None:
            return

        task_id = item.data(Qt.ItemDataRole.UserRole)
        source_date = item.data(Qt.ItemDataRole.UserRole + 1)
        if not task_id or not source_date:
            return

        mime_data = QMimeData()
        payload = json.dumps({"task_id": task_id, "source_date": source_date})
        mime_data.setData("application/x-task-move", payload.encode("utf-8"))

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec(Qt.DropAction.MoveAction)


class DayCell(QFrame):
    clicked = pyqtSignal(str)
    task_dropped = pyqtSignal(str, str, str)

    def __init__(self, day_date: date, current_month: int, tasks=None, selected=False, parent=None):
        super().__init__(parent)
        self.day_date = day_date
        self.date_str = date_key(day_date)
        self.current_month = current_month
        self.tasks = tasks or []
        self.selected = selected

        self.setAcceptDrops(True)
        self.setObjectName("DayCell")
        self.setMinimumSize(120, 105)
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 6, 8, 6)
        self.layout.setSpacing(4)

        self.day_label = QLabel(str(day_date.day))
        self.day_label.setObjectName("DayNumber")
        self.layout.addWidget(self.day_label)

        self.preview_container = QVBoxLayout()
        self.preview_container.setSpacing(3)
        self.layout.addLayout(self.preview_container)
        self.layout.addStretch()

        self.refresh_ui()

    def refresh_ui(self):
        self.day_label.setText(str(self.day_date.day))

        while self.preview_container.count():
            item = self.preview_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.setProperty("outOfMonth", self.day_date.month != self.current_month)
        self.setProperty("selected", self.selected)
        self.style().unpolish(self)
        self.style().polish(self)

        preview_tasks = sorted(self.tasks, key=lambda x: x["time"])[:3]
        for task in preview_tasks:
            badge = QLabel(f"{task['time']} {task['title'][:16]}")
            badge.setObjectName("PreviewBadge")
            badge.setStyleSheet(
                f"""
                QLabel {{
                    background-color: {CATEGORY_BG.get(task['category'], '#111827')};
                    color: {CATEGORY_COLORS.get(task['category'], '#E5E7EB')};
                    border: 1px solid {CATEGORY_COLORS.get(task['category'], '#374151')};
                    border-radius: 6px;
                    padding: 2px 6px;
                    font-size: 10px;
                }}
                """
            )
            self.preview_container.addWidget(badge)

        remaining = max(0, len(self.tasks) - 3)
        if remaining:
            more_label = QLabel(f"+{remaining} more")
            more_label.setStyleSheet("color: #94A3B8; font-size: 10px;")
            self.preview_container.addWidget(more_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.date_str)
        super().mousePressEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-task-move"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not event.mimeData().hasFormat("application/x-task-move"):
            event.ignore()
            return

        try:
            raw = bytes(event.mimeData().data("application/x-task-move")).decode("utf-8")
            data = json.loads(raw)
            task_id = data["task_id"]
            source_date = data["source_date"]
            self.task_dropped.emit(source_date, self.date_str, task_id)
            event.acceptProposedAction()
        except Exception:
            event.ignore()


class PomodoroDialog(QDialog):
    def __init__(self, parent=None, task_name: str = ""):
        super().__init__(parent)
        self.setWindowTitle("🍅 Pomodoro Timer")
        self.setModal(True)
        self.resize(300, 200)
        self.task_name = task_name
        self.remaining_seconds = 25 * 60  # 25 minutes
        self.is_running = False

        layout = QVBoxLayout(self)

        task_label = QLabel(f"Task: {task_name[:40]}")
        task_label.setStyleSheet("font-weight: bold; color: #00FF9C;")
        layout.addWidget(task_label)

        self.timer_label = QLabel("25:00")
        self.timer_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #EF4444; text-align: center;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)

        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle_timer)
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.toggle_timer)
        self.pause_btn.setEnabled(False)
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_timer)

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.reset_btn)
        layout.addLayout(button_layout)

        close_btn = QPushButton("Done")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

    def toggle_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.timer.start(1000)
        else:
            self.is_running = False
            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.timer.stop()

    def tick(self):
        self.remaining_seconds -= 1
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.is_running = False
            self.timer_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #10B981; text-align: center;")
            self.timer_label.setText("DONE!")
            QMessageBox.information(self, "Pomodoro Complete", f"Great work! 🍅 Session complete for '{self.task_name}'")

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.remaining_seconds = 25 * 60
        self.timer_label.setText("25:00")
        self.timer_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #EF4444; text-align: center;")
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)


class MainWindow(QMainWindow):
    def __init__(self, app_icon: QIcon):
        super().__init__()
        self.storage = Storage()
        self.app_icon = app_icon

        self.today = date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.selected_date = date_key(self.today)
        self.loading_tasks = False

        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(self.app_icon)
        self.resize(1450, 900)

        self._build_ui()
        self.load_background()
        self._build_tray()
        self.apply_dark_theme()
        self.refresh_calendar()
        self.refresh_task_list()
        self.refresh_analytics()

        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(30000)

        self.check_reminders()
        self.show_todays_agenda()

    def load_background(self):
        try:
            # Get central widget
            central = self.centralWidget()
            if not central:
                return

            bg_file = self.storage.settings.get("background_file", "")

            # If no background file is set, try default bundled GIF
            if not bg_file:
                bg_file = resource_path("background.pgn")
            
            # If file doesn't exist at saved path, try bundled version
            if not os.path.exists(bg_file):
                bg_file = resource_path("background.pgn")
            
            # If still doesn't exist, give up
            if not os.path.exists(bg_file):
                return

            # Clean up old background
            if hasattr(self, "bg_label") and self.bg_label:
                try:
                    if hasattr(self, "bg_movie"):
                        self.bg_movie.stop()
                    self.bg_label.deleteLater()
                except:
                    pass

            # Create background label
            self.bg_label = QLabel(central)
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
            self.bg_label.setScaledContents(True)

            # Load GIF or image
            if bg_file.lower().endswith(".gif"):
                self.bg_movie = QMovie(bg_file)
                if self.bg_movie.isValid():
                    self.bg_label.setMovie(self.bg_movie)
                    self.bg_movie.start()
            else:
                # Use QPixmap for static images
                pixmap = QPixmap(bg_file)
                if not pixmap.isNull():
                    self.bg_label.setPixmap(pixmap)

            # Send to back and make transparent to mouse events
            self.bg_label.lower()
            self.bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        except Exception as e:
            pass  # Silently ignore background loading errors

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(12)

        header = QHBoxLayout()

        self.prev_btn = QPushButton("◀ Prev")
        self.prev_btn.clicked.connect(self.prev_month)

        self.today_btn = QPushButton("Today")
        self.today_btn.clicked.connect(self.go_today)

        self.next_btn = QPushButton("Next ▶")
        self.next_btn.clicked.connect(self.next_month)

        self.month_label = QLabel()
        self.month_label.setObjectName("MonthLabel")
        self.month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.add_task_btn = QPushButton("+ Add Task")
        self.add_task_btn.clicked.connect(self.open_add_task_dialog)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.open_settings)

        self.background_btn = QPushButton("Background")
        self.background_btn.clicked.connect(self.change_background)

        self.menu_btn = QPushButton("≡ Menu")
        self.menu_btn.clicked.connect(self.show_menu)

        header.addWidget(self.prev_btn)
        header.addWidget(self.today_btn)
        header.addWidget(self.month_label, 1)
        header.addWidget(self.settings_btn)
        header.addWidget(self.background_btn)
        header.addWidget(self.add_task_btn)
        header.addWidget(self.menu_btn)
        header.addWidget(self.next_btn)

        root.addLayout(header)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.calendar_container = QWidget()
        self.calendar_layout = QGridLayout(self.calendar_container)
        self.calendar_layout.setSpacing(8)
        self.calendar_layout.setContentsMargins(0, 0, 0, 0)
        splitter.addWidget(self.calendar_container)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(6, 0, 0, 0)
        right_layout.setSpacing(10)

        self.selected_label = QLabel()
        self.selected_label.setObjectName("SelectedDateLabel")
        right_layout.addWidget(self.selected_label)

        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter tasks by title...")
        self.search_input.textChanged.connect(self.on_search_changed)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        right_layout.addLayout(search_layout)

        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Time", "Duration", "Category"])
        self.sort_combo.currentTextChanged.connect(self.on_sort_changed)
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo, 1)
        right_layout.addLayout(sort_layout)

        task_controls = QHBoxLayout()
        self.complete_hint = QLabel("Right-click tasks to edit/duplicate/delete. Press N for new task, Del to remove.")
        self.complete_hint.setStyleSheet("color: #94A3B8; font-size: 11px;")
        task_controls.addWidget(self.complete_hint, 1)
        right_layout.addLayout(task_controls)

        self.task_list = DraggableTaskList(main_window=self)
        self.task_list.itemChanged.connect(self.handle_task_checked)
        right_layout.addWidget(self.task_list, 1)

        # Quick actions bar
        quick_actions = QHBoxLayout()
        self.snooze_btn = QPushButton("⏰ Snooze")
        self.snooze_btn.setMaximumWidth(100)
        self.snooze_btn.clicked.connect(self.snooze_task)
        self.pomodo_btn = QPushButton("🍅 Pomodoro")
        self.pomodo_btn.setMaximumWidth(100)
        self.pomodo_btn.clicked.connect(self.start_pomodoro)
        quick_actions.addWidget(self.snooze_btn)
        quick_actions.addWidget(self.pomodo_btn)
        quick_actions.addStretch()
        right_layout.addLayout(quick_actions)

        analytics_group = QGroupBox("Weekly Analytics")
        analytics_layout = QVBoxLayout(analytics_group)

        self.analytics_week_label = QLabel()
        self.analytics_total_label = QLabel()
        self.analytics_coding_label = QLabel()
        self.analytics_work_label = QLabel()
        self.analytics_personal_label = QLabel()
        self.analytics_urgent_label = QLabel()
        self.analytics_completed_label = QLabel()

        analytics_layout.addWidget(self.analytics_week_label)
        analytics_layout.addWidget(self.analytics_completed_label)
        analytics_layout.addWidget(self.analytics_total_label)
        analytics_layout.addWidget(self.analytics_coding_label)
        analytics_layout.addWidget(self.analytics_work_label)
        analytics_layout.addWidget(self.analytics_personal_label)
        analytics_layout.addWidget(self.analytics_urgent_label)

        right_layout.addWidget(analytics_group)

        splitter.addWidget(right_panel)
        splitter.setSizes([980, 420])
        root.addWidget(splitter)

    def change_background(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Background",
            "",
            "Images (*.png *.jpg *.jpeg *.gif)",
        )

        if not file_path:
            return

        self.storage.settings["background_file"] = file_path
        self.storage.save_settings()
        self.load_background()

    def show_menu(self):
        menu = QMenu(self)
        export_action = menu.addAction("Export to CSV")
        import_action = menu.addAction("Import from CSV")
        menu.addSeparator()
        about_action = menu.addAction("About")

        action = menu.exec(self.menu_btn.mapToGlobal(self.menu_btn.rect().bottomLeft()))
        if action == export_action:
            self.export_to_csv()
        elif action == import_action:
            self.import_from_csv()
        elif action == about_action:
            QMessageBox.information(
                self,
                "About Cyber Planner",
                "╔════════════════════════════════════════╗\n"
                "║     CYBER PLANNER v2.0                 ║\n"
                "║  Advanced Task Management System       ║\n"
                "╚════════════════════════════════════════╝\n\n"
                "A powerful, dark-themed task scheduling and planning\n"
                "application built with PyQt6 for maximum productivity.\n\n"
                "✨ KEY FEATURES:\n"
                "  • Full calendar with month navigation\n"
                "  • Task creation with priority & recurring options\n"
                "  • Pomodoro timer (25min productivity sessions)\n"
                "  • Task reminders (15min, 5min, at-time)\n"
                "  • Discord webhook notifications\n"
                "  • CSV import/export for data portability\n"
                "  • Weekly analytics dashboard\n"
                "  • Drag-drop tasks between dates\n"
                "  • Custom backgrounds (images/GIFs)\n"
                "  • System tray integration\n\n"
                "⌨️  KEYBOARD SHORTCUTS:\n"
                "  N - Create new task\n"
                "  Del - Delete selected task\n\n"
                "👨‍💻 MADE BY:\n"
                "  galmx (xdrew87)\n"
                "  https://github.com/xdrew87\n\n"
                "📝 LICENSE:\n"
                "  © 2026 - All rights reserved.\n"
                "  Custom use only.",
            )

    def show_todays_agenda(self):
        today_tasks = self.storage.get_tasks_for_date(date_key(date.today()))
        if not today_tasks:
            return

        today_tasks.sort(key=lambda x: x["time"])
        msg = "📅 Today's Agenda:\n\n"
        total_hours = 0
        for task in today_tasks:
            duration = task.get("duration_minutes", 0)
            total_hours += duration / 60
            msg += f"{task['time']} - {task['title']} ({duration}m) [{task['category']}]\n"
        msg += f"\nTotal: {total_hours:.1f}h"

        self.show_tray_message("Today's Agenda", f"{len(today_tasks)} tasks scheduled")

    def resizeEvent(self, event):
        if hasattr(self, "bg_label"):
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def _build_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.app_icon)
        self.tray.setToolTip(APP_NAME)

        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.showNormal)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_from_tray)

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray.setContextMenu(tray_menu)
        self.tray.show()

    def quit_from_tray(self):
        self.tray.hide()
        QApplication.instance().quit()

    def apply_dark_theme(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#05080F"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#D7E3F4"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#0B1220"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#111827"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#0B1220"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#D7E3F4"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#D7E3F4"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#0F172A"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#D7E3F4"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#00FF9C"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#04120C"))
        self.setPalette(palette)

        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background-color: #05080F;
                color: #D7E3F4;
                font-family: Consolas, 'Segoe UI', monospace;
                font-size: 13px;
            }

            QPushButton {
                background-color: #0F172A;
                color: #D7E3F4;
                border: 1px solid #1E293B;
                border-radius: 10px;
                padding: 10px 14px;
            }

            QPushButton:hover {
                border: 1px solid #00FF9C;
                background-color: #111B30;
            }

            QPushButton:pressed {
                background-color: #0B1324;
            }

            QLabel#MonthLabel {
                font-size: 26px;
                font-weight: bold;
                color: #00FF9C;
                padding: 6px;
            }

            QLabel#SelectedDateLabel {
                font-size: 18px;
                font-weight: bold;
                color: #7DD3FC;
                padding: 4px 0px;
            }

            QGroupBox {
                border: 1px solid #1E293B;
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #08111E;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                color: #00FF9C;
                font-weight: bold;
            }

            QListWidget {
                background-color: #08111E;
                border: 1px solid #1E293B;
                border-radius: 12px;
                padding: 8px;
            }

            QListWidget::item {
                border-radius: 10px;
                padding: 10px;
                margin: 2px 0px;
            }

            QListWidget::item:selected {
                border: 1px solid #00FF9C;
            }

            QLineEdit, QComboBox, QTimeEdit, QSpinBox {
                background-color: #0B1220;
                color: #D7E3F4;
                border: 1px solid #243244;
                border-radius: 8px;
                padding: 8px;
            }

            QDialog {
                background-color: #05080F;
            }

            QFrame#DayCell {
                background-color: #08111E;
                border: 1px solid #1E293B;
                border-radius: 12px;
            }

            QFrame#DayCell[selected="true"] {
                border: 2px solid #00FF9C;
                background-color: #0A1424;
            }

            QFrame#DayCell[outOfMonth="true"] {
                background-color: #060B14;
                border: 1px solid #121B2B;
            }

            QLabel#DayNumber {
                font-size: 16px;
                font-weight: bold;
                color: #E2E8F0;
            }
            """
        )

    def edit_task(self, item: QListWidgetItem):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        task = None
        for t in self.storage.get_tasks_for_date(self.selected_date):
            if t["id"] == task_id:
                task = t
                break

        if not task:
            return

        categories = self.storage.settings.get("custom_categories", ["Work", "Personal", "Urgent", "Coding"])
        dialog = AddTaskDialog(self, self.selected_date, task, categories)
        if dialog.exec():
            updated_task = dialog.get_task()
            self.storage.update_task(self.selected_date, updated_task)
            self.refresh_task_list()
            self.refresh_calendar()
            self.refresh_analytics()

    def duplicate_task(self, item: QListWidgetItem):
        try:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            task = None
            for t in self.storage.get_tasks_for_date(self.selected_date):
                if t["id"] == task_id:
                    task = t.copy()
                    break

            if not task:
                QMessageBox.warning(self, "Error", "Task not found.")
                return

            task["id"] = str(uuid.uuid4())
            task["created_at"] = datetime.now().isoformat()
            task["reminders_sent"] = []
            self.storage.add_task(self.selected_date, task)
            self.refresh_task_list()
            self.refresh_calendar()
            self.refresh_analytics()
            QMessageBox.information(self, "Duplicated", f"Task '{task['title']}' duplicated.")
        except Exception as e:
            QMessageBox.critical(self, "Duplicate Error", f"Failed to duplicate task: {str(e)}")

    def delete_task_from_menu(self, item: QListWidgetItem):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(self, "Delete", "Delete this task?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.storage.delete_task(self.selected_date, task_id)
            self.refresh_task_list()
            self.refresh_calendar()
            self.refresh_analytics()

    def on_search_changed(self, text: str):
        self.refresh_task_list()

    def on_sort_changed(self, text: str):
        self.refresh_task_list()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_N and event.modifiers() == Qt.KeyboardModifier.NoModifier:
            self.open_add_task_dialog()
        elif event.key() == Qt.Key.Key_Delete:
            item = self.task_list.currentItem()
            if item:
                self.delete_task_from_menu(item)
        else:
            super().keyPressEvent(event)

    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Tasks", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return

        try:
            import csv
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Time", "Title", "Duration (min)", "Category", "Notes"])
                for date_str, tasks in sorted(self.storage.tasks.items()):
                    for task in tasks:
                        writer.writerow([
                            date_str,
                            task.get("time", ""),
                            task.get("title", ""),
                            task.get("duration_minutes", ""),
                            task.get("category", ""),
                            task.get("notes", ""),
                        ])
            QMessageBox.information(self, "Exported", f"Tasks exported to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export: {str(e)}")

    def import_from_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Tasks", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return

        try:
            import csv
            count = 0
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    date_str = row.get("Date", "")
                    if not date_str:
                        continue
                    task = {
                        "id": str(uuid.uuid4()),
                        "title": row.get("Title", ""),
                        "time": row.get("Time", "09:00"),
                        "duration_minutes": int(row.get("Duration (min)", 60)),
                        "category": row.get("Category", "Work"),
                        "notes": row.get("Notes", ""),
                        "created_at": datetime.now().isoformat(),
                        "reminders_sent": [],
                    }
                    self.storage.add_task(date_str, task)
                    count += 1
            self.refresh_calendar()
            self.refresh_task_list()
            self.refresh_analytics()
            QMessageBox.information(self, "Imported", f"Imported {count} tasks.")
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import: {str(e)}")

    def open_settings(self):
        settings_copy = dict(self.storage.settings)
        env_override = os.getenv("DISCORD_WEBHOOK_URL")
        if env_override:
            settings_copy["discord_webhook_url"] = env_override

        dialog = SettingsDialog(self, settings_copy)
        if dialog.exec():
            updated = dialog.get_settings()
            self.storage.settings.update(updated)
            self.storage.save_settings()
            QMessageBox.information(self, "Saved", "Settings updated successfully.")

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.refresh_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.refresh_calendar()

    def go_today(self):
        self.today = date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.selected_date = date_key(self.today)
        self.refresh_calendar()
        self.refresh_task_list()
        self.refresh_analytics()

    def refresh_calendar(self):
        self.month_label.setText(f"{calendar.month_name[self.current_month]} {self.current_year}")

        while self.calendar_layout.count():
            item = self.calendar_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, name in enumerate(weekday_names):
            label = QLabel(name)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(
                "font-weight: bold; color: #00FF9C; background-color: #08111E; "
                "border: 1px solid #1E293B; border-radius: 8px; padding: 8px;"
            )
            self.calendar_layout.addWidget(label, 0, col)

        cal = calendar.Calendar(firstweekday=0)
        month_matrix = cal.monthdatescalendar(self.current_year, self.current_month)

        for row_idx, week in enumerate(month_matrix, start=1):
            for col_idx, day_dt in enumerate(week):
                tasks = self.storage.get_tasks_for_date(date_key(day_dt))
                cell = DayCell(
                    day_dt,
                    self.current_month,
                    tasks=tasks,
                    selected=(date_key(day_dt) == self.selected_date),
                )
                cell.clicked.connect(self.select_date)
                cell.task_dropped.connect(self.handle_task_drop)
                self.calendar_layout.addWidget(cell, row_idx, col_idx)

    def select_date(self, selected_date_str: str):
        self.selected_date = selected_date_str
        selected_dt = parse_date_key(selected_date_str)
        self.current_year = selected_dt.year
        self.current_month = selected_dt.month
        self.refresh_calendar()
        self.refresh_task_list()
        self.refresh_analytics()

    def refresh_task_list(self):
        self.loading_tasks = True
        self.task_list.clear()

        selected_dt = parse_date_key(self.selected_date)
        self.selected_label.setText(f"Tasks for {selected_dt.strftime('%A, %B %d, %Y')}")

        tasks = list(self.storage.get_tasks_for_date(self.selected_date))
        
        # Filter by search
        search_text = self.search_input.text().lower()
        if search_text:
            tasks = [t for t in tasks if search_text in t["title"].lower() or search_text in t.get("notes", "").lower()]

        # Sort by priority first, then by selected sort
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        tasks.sort(key=lambda x: priority_order.get(x.get("priority", "Medium"), 1))

        sort_by = self.sort_combo.currentText()
        if sort_by == "Time":
            tasks.sort(key=lambda x: x["time"])
        elif sort_by == "Duration":
            tasks.sort(key=lambda x: x["duration_minutes"], reverse=True)
        elif sort_by == "Category":
            tasks.sort(key=lambda x: x["category"])

        for task in tasks:
            duration = task.get("duration_minutes", 60)
            priority = task.get("priority", "Medium")
            recurring = task.get("recurring", "None")
            notes_preview = f" | {task.get('notes', '')[:20]}" if task.get('notes') else ""
            
            # Priority badge
            priority_badge = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
            recurring_badge = "🔄 " if recurring != "None" else ""
            
            duration_bar = "▓" * max(1, min(10, duration // 30))
            text = f"{task['time']} {duration_bar} {priority_badge} {duration}m | {recurring_badge}{task['title']}{notes_preview}"
            
            item = QListWidgetItem(text)
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsSelectable
                | Qt.ItemFlag.ItemIsDragEnabled
            )
            item.setCheckState(Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, task["id"])
            item.setData(Qt.ItemDataRole.UserRole + 1, self.selected_date)

            fg = QColor(CATEGORY_COLORS.get(task["category"], "#D7E3F4"))
            bg = QColor(CATEGORY_BG.get(task["category"], "#111827"))
            item.setForeground(fg)
            item.setBackground(bg)

            self.task_list.addItem(item)

        self.loading_tasks = False

    def open_add_task_dialog(self):
        categories = self.storage.settings.get("custom_categories", ["Work", "Personal", "Urgent", "Coding"])
        dialog = AddTaskDialog(self, self.selected_date, None, categories)
        if dialog.exec():
            task = dialog.get_task()
            self.storage.add_task(self.selected_date, task)
            self.refresh_task_list()
            self.refresh_calendar()
            self.refresh_analytics()

    def handle_task_checked(self, item: QListWidgetItem):
        if self.loading_tasks:
            return

        if item.checkState() == Qt.CheckState.Checked:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            task = None
            for t in self.storage.get_tasks_for_date(self.selected_date):
                if t["id"] == task_id:
                    task = t
                    break

            if not task:
                item.setCheckState(Qt.CheckState.Unchecked)
                return

            # Ask for confirmation before deleting
            reply = QMessageBox.question(
                self,
                "Complete Task",
                f"Mark '{task['title']}' as complete and delete it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                # User clicked No, uncheck the item
                item.setCheckState(Qt.CheckState.Unchecked)
                return

            # Handle recurring tasks
            if task.get("recurring") != "None":
                self.generate_next_recurring_task(task)

            self.storage.delete_task(self.selected_date, task_id)
            self.refresh_task_list()
            self.refresh_calendar()
            self.refresh_analytics()

    def generate_next_recurring_task(self, task: dict):
        """Generate next occurrence of recurring task"""
        recurring_type = task.get("recurring", "None")
        if recurring_type == "None":
            return

        current_date = parse_date_key(self.selected_date)
        if recurring_type == "Daily":
            next_date = current_date + timedelta(days=1)
        elif recurring_type == "Weekly":
            next_date = current_date + timedelta(weeks=1)
        elif recurring_type == "Monthly":
            try:
                next_date = current_date + timedelta(days=30)
            except:
                next_date = current_date + timedelta(days=28)
        else:
            return

        # Create new task for next occurrence
        new_task = task.copy()
        new_task["id"] = str(uuid.uuid4())
        new_task["created_at"] = datetime.now().isoformat()
        new_task["reminders_sent"] = []
        
        self.storage.add_task(date_key(next_date), new_task)

    def snooze_task(self):
        """Move selected task to tomorrow"""
        item = self.task_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Task", "Please select a task to snooze.")
            return

        task_id = item.data(Qt.ItemDataRole.UserRole)
        task = None
        for t in self.storage.get_tasks_for_date(self.selected_date):
            if t["id"] == task_id:
                task = t.copy()
                break

        if not task:
            return

        tomorrow = parse_date_key(self.selected_date) + timedelta(days=1)
        task["id"] = str(uuid.uuid4())
        task["reminders_sent"] = []

        self.storage.add_task(date_key(tomorrow), task)
        self.storage.delete_task(self.selected_date, task_id)
        self.refresh_task_list()
        self.refresh_calendar()
        self.refresh_analytics()
        QMessageBox.information(self, "Snoozed", f"Task moved to tomorrow ({date_key(tomorrow)}).")

    def start_pomodoro(self):
        """Start a 25-minute Pomodoro timer"""
        item = self.task_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Task", "Please select a task for Pomodoro.")
            return

        task_title = item.text().split("|")[-1].strip() if "|" in item.text() else item.text()[:30]

        self.pomodoro_dialog = PomodoroDialog(self, task_title)
        self.pomodoro_dialog.exec()

    def closeEvent(self, event):
        if self.tray.isVisible():
            self.hide()
            self.show_tray_message(APP_NAME, "Still running in system tray.")
            event.ignore()
        else:
            event.accept()

    def handle_task_drop(self, source_date: str, target_date: str, task_id: str):
        if source_date == target_date:
            return
        moved = self.storage.move_task(source_date, target_date, task_id)
        if moved:
            self.refresh_calendar()
            self.refresh_task_list()
            self.refresh_analytics()

    def get_week_range(self, ref_date: date):
        start = ref_date - timedelta(days=ref_date.weekday())
        end = start + timedelta(days=6)
        return start, end

    def refresh_analytics(self):
        selected_dt = parse_date_key(self.selected_date)
        week_start, week_end = self.get_week_range(selected_dt)

        totals = {"Work": 0, "Personal": 0, "Urgent": 0, "Coding": 0}
        total_minutes = 0
        total_tasks = 0

        current = week_start
        while current <= week_end:
            ds = date_key(current)
            for task in self.storage.get_tasks_for_date(ds):
                mins = int(task.get("duration_minutes", 0))
                total_minutes += mins
                category = task.get("category", "Work")
                totals[category] = totals.get(category, 0) + mins
                total_tasks += 1
            current += timedelta(days=1)

        self.analytics_week_label.setText(
            f"Week: {week_start.strftime('%b %d')} → {week_end.strftime('%b %d, %Y')}"
        )
        self.analytics_completed_label.setText(f"Total tasks: {total_tasks}")
        self.analytics_total_label.setText(f"Total scheduled time: {pretty_hours(total_minutes)}")
        self.analytics_coding_label.setText(f"Coding: {pretty_hours(totals['Coding'])}")
        self.analytics_work_label.setText(f"Work: {pretty_hours(totals['Work'])}")
        self.analytics_personal_label.setText(f"Personal: {pretty_hours(totals['Personal'])}")
        self.analytics_urgent_label.setText(f"Urgent: {pretty_hours(totals['Urgent'])}")

    def show_tray_message(self, title: str, message: str):
        if not self.storage.settings.get("tray_notifications_enabled", True):
            return
        if self.tray.isVisible():
            self.tray.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                8000,
            )

    def send_discord_webhook(self, title: str, message: str):
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL") or self.storage.settings.get(
            "discord_webhook_url", ""
        )
        if not webhook_url.strip():
            return

        payload = {
            "username": "Cyber Planner",
            "embeds": [
                {
                    "title": title,
                    "description": message,
                    "color": 0x00FF9C,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            ],
        }

        try:
            requests.post(webhook_url, json=payload, timeout=8)
        except Exception:
            pass

    def check_reminders(self):
        if not self.storage.settings.get("reminders_enabled", True):
            return

        now = datetime.now()

        for ds, tasks in list(self.storage.tasks.items()):
            for task in list(tasks):
                try:
                    task_dt = combine_date_time(ds, task["time"])
                except Exception:
                    continue

                for offset in REMINDER_OFFSETS_MINUTES:
                    reminder_key = f"{ds}|{offset}"
                    send_at = task_dt - timedelta(minutes=offset)

                    if send_at <= now < send_at + timedelta(seconds=59):
                        sent = task.get("reminders_sent", [])
                        if reminder_key in sent:
                            continue

                        if offset == 0:
                            title = "Task Due Now"
                            body = f"{task['title']} [{task['category']}] at {task['time']}"
                        else:
                            title = f"Task Reminder ({offset} min)"
                            body = f"{task['title']} [{task['category']}] at {task['time']}"

                        self.show_tray_message(title, body)
                        self.send_discord_webhook(title, body)

                        task.setdefault("reminders_sent", []).append(reminder_key)
                        self.storage.update_task(ds, task)

    def closeEvent(self, event):
        if self.tray.isVisible():
            self.hide()
            self.show_tray_message(APP_NAME, "Still running in system tray.")
            event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    icon_path = resource_path(ICON_FILE)
    app_icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()
    if not app_icon.isNull():
        app.setWindowIcon(app_icon)

    window = MainWindow(app_icon)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
