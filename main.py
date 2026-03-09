"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         CYBER PLANNER v2.5                                   ║
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
import hashlib
import shutil
from datetime import datetime, timedelta, date

import requests
from PyQt6.QtCore import Qt, QMimeData, QTimer, pyqtSignal, QRect, QSize
from PyQt6.QtGui import QAction, QDrag, QIcon, QColor, QPalette, QMovie, QPixmap, QFont
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
    QTabWidget,
    QScrollArea,
)

APP_NAME = "Cyber Planner"
TASKS_FILE = "tasks.json"
SETTINGS_FILE = "settings.json"
CREDENTIALS_FILE = "credentials.json"
PROFILES_DIR = "profiles"
ICON_FILE = "cyber_planner2.ico"

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

BACKGROUND_FILE = "200.gif"   # can also be .gif
BACKGROUND_OPACITY = 0.18           # transparency so UI stays readable

MOTIVATIONAL_QUOTES = [
    "Every task completed is a victory! 🎯",
    "Small progress is still progress! 📈",
    "You're doing great! Keep it up! 💪",
    "Success is built one task at a time! 🏢",
    "Your dedication today shapes tomorrow! ⭐",
    "Stay focused, stay productive! 🚀",
    "Every minute counts! ⏱️",
    "You've got this! Believe in yourself! 💯",
    "Organize, prioritize, accomplish! ✨",
    "Today is your day to shine! 🌟",
    "Progress over perfection! 🎨",
    "You are one day closer to your goals! 🎯",
    "Seize the day! 🌅",
    "Make it happen! 🔥",
    "Your effort will pay off! 💎",
]

# THEME DEFINITIONS
THEMES = {
    "Cyberpunk": {
        "bg": "#05080F",
        "accent": "#00FF9C",
        "secondary": "#7DD3FC",
        "danger": "#EF4444",
        "text": "#D7E3F4",
        "border": "#243244",
    },
    "Purple Dream": {
        "bg": "#0F0B1E",
        "accent": "#B366FF",
        "secondary": "#9945FF",
        "danger": "#FF6B9D",
        "text": "#E0D5FF",
        "border": "#3D2E5F",
    },
    "Ocean Blue": {
        "bg": "#0A1628",
        "accent": "#00D9FF",
        "secondary": "#0099FF",
        "danger": "#FF4444",
        "text": "#B8D4E8",
        "border": "#1E4D6D",
    },
    "Neon Pink": {
        "bg": "#1A0F15",
        "accent": "#FF0080",
        "secondary": "#FF1493",
        "danger": "#FF6347",
        "text": "#FFB3D9",
        "border": "#662E4E",
    },
}

# SOUND NOTIFICATIONS
SOUND_ALERTS = {
    "High": "alert",      # High priority beep
    "Medium": "notify",   # Medium beep
    "Low": "chime",       # Soft chime
}


def resource_path(relative_path: str) -> str:
    """
    Return the correct absolute path for local runs and PyInstaller builds.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def play_sound(sound_type: str = "notify"):
    """Play system sound notification"""
    try:
        import winsound
        frequencies = {"alert": 1000, "notify": 800, "chime": 600}
        frequency = frequencies.get(sound_type, 800)
        duration = 200  # milliseconds
        winsound.Beep(frequency, duration)
    except:
        pass  # Fail silently if winsound not available


def get_theme_colors(theme_name: str = "Cyberpunk") -> dict:
    """Get color palette for theme"""
    return THEMES.get(theme_name, THEMES["Cyberpunk"])


def hash_password(password: str) -> str:
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def ensure_credentials():
    """Ensure credentials file exists with default admin account"""
    if not os.path.exists(CREDENTIALS_FILE):
        default_creds = {
            "accounts": {
                "admin": {
                    "password_hash": hash_password("admin123"),
                    "created_at": datetime.now().isoformat(),
                    "profiles": ["Main Profile"],
                    "default_profile": "Main Profile"
                }
            }
        }
        with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_creds, f, indent=4)
    return True


def verify_credentials(username: str, password: str) -> bool:
    """Verify username and password"""
    ensure_credentials()
    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            creds = json.load(f)
        accounts = creds.get("accounts", {})
        if username not in accounts:
            return False
        stored_hash = accounts[username].get("password_hash", "")
        return stored_hash == hash_password(password)
    except:
        return False


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


def ensure_profiles_directory():
    """Create profiles directory if it doesn't exist"""
    if not os.path.exists(PROFILES_DIR):
        os.makedirs(PROFILES_DIR, exist_ok=True)


def get_profile_tasks_file(username: str, profile_name: str) -> str:
    """Get the tasks file path for a specific user profile"""
    ensure_profiles_directory()
    safe_username = username.replace(" ", "_").lower()
    safe_profile = profile_name.replace(" ", "_").lower()
    return os.path.join(PROFILES_DIR, f"{safe_username}_{safe_profile}_tasks.json")


def get_profile_settings_file(username: str, profile_name: str) -> str:
    """Get the settings file path for a specific user profile"""
    ensure_profiles_directory()
    safe_username = username.replace(" ", "_").lower()
    safe_profile = profile_name.replace(" ", "_").lower()
    return os.path.join(PROFILES_DIR, f"{safe_username}_{safe_profile}_settings.json")


def get_user_profiles(username: str) -> list:
    """Get list of profiles for a user"""
    ensure_credentials()
    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            creds = json.load(f)
        accounts = creds.get("accounts", {})
        return accounts.get(username, {}).get("profiles", ["Main Profile"])
    except:
        return ["Main Profile"]


def add_user_profile(username: str, profile_name: str):
    """Add a new profile for a user"""
    ensure_credentials()
    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            creds = json.load(f)
        
        if username in creds.get("accounts", {}):
            profiles = creds["accounts"][username].get("profiles", ["Main Profile"])
            if profile_name not in profiles:
                profiles.append(profile_name)
                creds["accounts"][username]["profiles"] = profiles
                
                with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
                    json.dump(creds, f, indent=4)
                return True
    except:
        pass
    return False


class Storage:
    def __init__(self):
        self.tasks_file = TASKS_FILE
        self.settings_file = SETTINGS_FILE
        
        self.tasks = load_json(self.tasks_file, {})
        self.settings = load_json(
            self.settings_file,
            {
                "discord_webhook_url": "",
                "reminders_enabled": True,
                "tray_notifications_enabled": True,
                "background_file": "",
                "custom_categories": ["Work", "Personal", "Urgent", "Coding"],
                "profile_color": "#00FF9C",
                "theme": "dark",
                "sound_alerts_enabled": True,
                "theme_name": "Cyberpunk",
                # Advanced settings
                "work_hours_enabled": False,
                "work_start_hour": 9,
                "work_end_hour": 18,
                "pomodoro_duration": 25,
                "break_duration": 5,
                "font_size": "Medium",
                "weekly_goal_hours": 40,
                "auto_backup_enabled": True,
                "auto_backup_frequency": "daily",
                "always_on_top": False,
                "notification_position": "bottom-right",
                "dark_mode_schedule": False,
                "auto_sunset_sunrise": False,
            },
        )

    def save_tasks(self):
        save_json(self.tasks_file, self.tasks)

    def save_settings(self):
        save_json(self.settings_file, self.settings)

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

    def mark_task_complete(self, date_str: str, task_id: str, completed: bool = True):
        """Mark a task as complete/incomplete with timestamp"""
        if date_str not in self.tasks:
            return False
        for task in self.tasks[date_str]:
            if task["id"] == task_id:
                task["completed"] = completed
                task["completed_at"] = datetime.now().isoformat() if completed else None
                self.save_tasks()
                return True
        return False

    def get_productivity_stats(self, date_range_days: int = 7) -> dict:
        """Calculate productivity stats for the past N days"""
        end_date = date.today()
        start_date = end_date - timedelta(days=date_range_days-1)
        
        stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "completion_rate": 0.0,
            "total_hours_planned": 0.0,
            "by_category": {},
            "by_day": {}
        }
        
        current = start_date
        while current <= end_date:
            day_key = date_key(current)
            day_tasks = self.tasks.get(day_key, [])
            stats["by_day"][day_key] = {
                "completed": sum(1 for t in day_tasks if t.get("completed", False)),
                "total": len(day_tasks),
                "hours": sum(t.get("duration_minutes", 0) for t in day_tasks) / 60
            }
            
            for task in day_tasks:
                stats["total_tasks"] += 1
                if task.get("completed", False):
                    stats["completed_tasks"] += 1
                stats["total_hours_planned"] += task.get("duration_minutes", 0) / 60
                
                category = task.get("category", "Other")
                if category not in stats["by_category"]:
                    stats["by_category"][category] = {"total": 0, "completed": 0}
                stats["by_category"][category]["total"] += 1
                if task.get("completed", False):
                    stats["by_category"][category]["completed"] += 1
            
            current += timedelta(days=1)
        
        if stats["total_tasks"] > 0:
            stats["completion_rate"] = (stats["completed_tasks"] / stats["total_tasks"]) * 100
        
        return stats

    def init_habits(self):
        """Initialize habits if not present"""
        if "habits" not in self.settings:
            self.settings["habits"] = []
            self.save_settings()

    def add_habit(self, habit: dict):
        """Add a new habit"""
        self.init_habits()
        habit["id"] = habit.get("id", str(uuid.uuid4()))
        habit["created_at"] = habit.get("created_at", datetime.now().isoformat())
        habit["streak"] = 0
        habit["completed_dates"] = []
        self.settings["habits"].append(habit)
        self.save_settings()

    def complete_habit_today(self, habit_id: str):
        """Mark habit as completed for today"""
        self.init_habits()
        today = date_key(date.today())
        for habit in self.settings["habits"]:
            if habit["id"] == habit_id:
                if today not in habit.get("completed_dates", []):
                    habit.setdefault("completed_dates", []).append(today)
                    self._update_habit_streak(habit)
                    self.save_settings()
                    return True
        return False

    def _update_habit_streak(self, habit: dict):
        """Update streak based on completed dates"""
        completed = habit.get("completed_dates", [])
        if not completed:
            habit["streak"] = 0
            return
        
        sorted_dates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in completed])
        today = date.today()
        streak = 0
        current = today
        
        for check_date in reversed(sorted_dates):
            if (current - check_date).days == 0:
                streak += 1
                current = check_date
            elif (current - check_date).days == 1:
                streak += 1
                current = check_date
            else:
                break
        
        habit["streak"] = streak

    def get_habit_streak(self, habit_id: str) -> int:
        """Get current streak for a habit"""
        self.init_habits()
        for habit in self.settings["habits"]:
            if habit["id"] == habit_id:
                return habit.get("streak", 0)
        return 0

    def delete_habit(self, habit_id: str):
        """Delete a habit"""
        self.init_habits()
        self.settings["habits"] = [h for h in self.settings["habits"] if h["id"] != habit_id]
        self.save_settings()

    def get_smart_suggestions(self) -> list:
        """Get smart task suggestions based on patterns"""
        suggestions = []
        current_hour = datetime.now().hour
        
        # Analyze task patterns
        all_tasks = []
        for day_key, task_list in self.tasks.items():
            all_tasks.extend(task_list)
        
        if not all_tasks:
            return []
        
        # Categorize by time of day
        morning_tasks = [t for t in all_tasks if 5 <= int(t.get("time", "12:00").split(":")[0]) < 12]
        afternoon_tasks = [t for t in all_tasks if 12 <= int(t.get("time", "12:00").split(":")[0]) < 17]
        evening_tasks = [t for t in all_tasks if 17 <= int(t.get("time", "12:00").split(":")[0]) < 22]
        
        # Suggest based on current time
        if 5 <= current_hour < 12 and morning_tasks:
            most_common_cat = max(set(t.get("category") for t in morning_tasks), 
                                 key=[t.get("category") for t in morning_tasks].count)
            suggestions.append(f"🌅 Good morning! Try working on {most_common_cat} tasks")
        elif 12 <= current_hour < 17 and afternoon_tasks:
            most_common_cat = max(set(t.get("category") for t in afternoon_tasks),
                                 key=[t.get("category") for t in afternoon_tasks].count)
            suggestions.append(f"☀️ Afternoon push! Focus on {most_common_cat}")
        elif 17 <= current_hour < 22 and evening_tasks:
            most_common_cat = max(set(t.get("category") for t in evening_tasks),
                                 key=[t.get("category") for t in evening_tasks].count)
            suggestions.append(f"🌙 Wind down with {most_common_cat}")
        
        # Suggest incomplete high-priority tasks
        incomplete_urgent = [t for t in all_tasks if t.get("priority") == "High" and not t.get("completed")]
        if incomplete_urgent:
            suggestions.append(f"⚡ {len(incomplete_urgent)} high-priority tasks waiting")
        
        return suggestions[:3]  # Return top 3 suggestions

    def get_daily_heatmap_data(self, days: int = 30) -> dict:
        """Get productivity data for heatmap (completion rate per day)"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        heatmap = {}
        current = start_date
        while current <= end_date:
            day_key = date_key(current)
            day_tasks = self.tasks.get(day_key, [])
            if day_tasks:
                completed = sum(1 for t in day_tasks if t.get("completed", False))
                rate = (completed / len(day_tasks)) * 100
                heatmap[day_key] = {
                    "completed": completed,
                    "total": len(day_tasks),
                    "rate": rate
                }
            else:
                heatmap[day_key] = {"completed": 0, "total": 0, "rate": 0}
            current += timedelta(days=1)
        
        return heatmap

    def get_burndown_data(self, days: int = 7) -> dict:
        """Get burndown data (planned vs completed over time)"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        burndown = {}
        cumulative_planned = 0
        cumulative_completed = 0
        
        current = start_date
        while current <= end_date:
            day_key = date_key(current)
            day_tasks = self.tasks.get(day_key, [])
            
            daily_planned = sum(t.get("duration_minutes", 0) for t in day_tasks) / 60
            daily_completed = sum(t.get("duration_minutes", 0) for t in day_tasks if t.get("completed", False)) / 60
            
            cumulative_planned += daily_planned
            cumulative_completed += daily_completed
            
            burndown[day_key] = {
                "planned": cumulative_planned,
                "completed": cumulative_completed,
                "remaining": max(0, cumulative_planned - cumulative_completed)
            }
            current += timedelta(days=1)
        
        return burndown





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

        self.energy_input = QComboBox()
        self.energy_input.addItems(["Low", "Medium", "High"])
        self.energy_input.setCurrentText("Medium")
        if task:
            self.energy_input.setCurrentText(task.get("energy_level", "Medium"))

        self.status_input = QComboBox()
        self.status_input.addItems(["Not Started", "In Progress", "Completed"])
        self.status_input.setCurrentText("Not Started")
        if task and task.get("completed", False):
            self.status_input.setCurrentText("Completed")

        form.addRow("Task Title", self.title_input)
        form.addRow("Time", self.time_input)
        form.addRow("Duration", duration_layout)
        form.addRow("Category", self.category_input)
        form.addRow("Priority", self.priority_input)
        form.addRow("Energy Level", self.energy_input)
        form.addRow("Recurring", self.recurring_input)
        form.addRow("Status", self.status_input)
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
            "energy_level": self.energy_input.currentText(),
            "recurring": self.recurring_input.currentText(),
            "notes": self.notes_input.toPlainText().strip(),
            "completed": self.status_input.currentText() == "Completed",
            "created_at": self.task.get("created_at", datetime.now().isoformat()) if self.task else datetime.now().isoformat(),
            "reminders_sent": self.task.get("reminders_sent", []) if self.task else [],
        }
        return task_data


class HabitDialog(QDialog):
    def __init__(self, parent=None, habit: dict = None):
        super().__init__(parent)
        self.habit = habit
        self.setWindowTitle("Edit Habit" if habit else "Add Habit")
        self.setModal(True)
        self.resize(400, 300)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Morning workout, Read 30min")
        if habit:
            self.name_input.setText(habit.get("name", ""))

        self.frequency_input = QComboBox()
        self.frequency_input.addItems(["Daily", "Weekdays", "Weekends", "Weekly"])
        if habit:
            self.frequency_input.setCurrentText(habit.get("frequency", "Daily"))

        self.category_input = QComboBox()
        self.category_input.addItems(["Health", "Learning", "Personal", "Work", "Fitness"])
        if habit:
            self.category_input.setCurrentText(habit.get("category", "Health"))

        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")
        if habit:
            habit_time = habit.get("reminder_time", "09:00")
            self.time_input.setTime(datetime.strptime(habit_time, "%H:%M").time())
        else:
            self.time_input.setTime(datetime.strptime("09:00", "%H:%M").time())

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Why is this habit important?")
        self.notes_input.setMaximumHeight(80)
        if habit:
            self.notes_input.setText(habit.get("notes", ""))

        form.addRow("Habit Name", self.name_input)
        form.addRow("Frequency", self.frequency_input)
        form.addRow("Category", self.category_input)
        form.addRow("Reminder Time", self.time_input)
        form.addRow("Notes", self.notes_input)
        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Error", "Habit name is required!")
            return
        self.accept()

    def get_habit(self):
        return {
            "id": self.habit["id"] if self.habit else str(uuid.uuid4()),
            "name": self.name_input.text().strip(),
            "frequency": self.frequency_input.currentText(),
            "category": self.category_input.currentText(),
            "reminder_time": self.time_input.time().toString("HH:mm"),
            "notes": self.notes_input.toPlainText().strip(),
            "created_at": self.habit.get("created_at", datetime.now().isoformat()) if self.habit else datetime.now().isoformat(),
        }


class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None, storage=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(500, 550)
        self.settings = settings or {}
        self.storage = storage
        self.categories = settings.get("custom_categories", []) if settings else []
        self.selected_bg = ""  # Initialize early to avoid AttributeError

        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        
        # ===== NOTIFICATIONS TAB =====
        notif_widget = QWidget()
        notif_layout = QVBoxLayout(notif_widget)
        notif_form = QFormLayout()

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

        self.sound_combo = QComboBox()
        self.sound_combo.addItems(["Enabled", "Disabled"])
        self.sound_combo.setCurrentText(
            "Enabled" if self.settings.get("sound_alerts_enabled", True) else "Disabled"
        )

        notif_form.addRow("Discord Webhook", self.webhook_input)
        notif_form.addRow("Reminders", self.reminders_combo)
        notif_form.addRow("Tray Notifications", self.tray_combo)
        notif_form.addRow("Sound Alerts", self.sound_combo)
        notif_layout.addLayout(notif_form)

        note = QLabel(
            "Security note: for production use, set DISCORD_WEBHOOK_URL as an environment variable."
        )
        note.setWordWrap(True)
        notif_layout.addWidget(note)
        notif_layout.addStretch()
        
        tabs.addTab(notif_widget, "🔔 Notifications")

        # ===== THEME TAB =====
        theme_widget = QWidget()
        theme_layout = QVBoxLayout(theme_widget)
        theme_form = QFormLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEMES.keys()))
        self.theme_combo.setCurrentText(self.settings.get("theme_name", "Cyberpunk"))
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)

        theme_form.addRow("Color Theme", self.theme_combo)
        theme_layout.addLayout(theme_form)

        # Theme preview
        self.theme_preview = QLabel()
        self.theme_preview.setStyleSheet("border: 2px solid #00FF9C; border-radius: 8px; padding: 20px;")
        self.theme_preview.setMinimumHeight(80)
        self.on_theme_changed()
        theme_layout.addWidget(self.theme_preview)
        theme_layout.addStretch()
        
        tabs.addTab(theme_widget, "🎨 Themes")

        # ===== TIME & SCHEDULE TAB =====
        time_widget = QWidget()
        time_layout = QVBoxLayout(time_widget)
        time_form = QFormLayout()

        self.work_hours_check = QComboBox()
        self.work_hours_check.addItems(["Disabled", "Enabled"])
        self.work_hours_check.setCurrentText("Enabled" if self.settings.get("work_hours_enabled", False) else "Disabled")
        
        self.work_start = QTimeEdit()
        self.work_start.setTime(datetime.strptime(f"{self.settings.get('work_start_hour', 9):02d}:00", "%H:%M").time())
        
        self.work_end = QTimeEdit()
        self.work_end.setTime(datetime.strptime(f"{self.settings.get('work_end_hour', 18):02d}:00", "%H:%M").time())

        time_form.addRow("Work Hours", self.work_hours_check)
        time_form.addRow("Start Time", self.work_start)
        time_form.addRow("End Time", self.work_end)
        
        time_note = QLabel("💡 Disable reminders outside work hours")
        time_note.setStyleSheet("color: #94A3B8; font-size: 10px;")
        time_layout.addLayout(time_form)
        time_layout.addWidget(time_note)
        time_layout.addStretch()
        
        tabs.addTab(time_widget, "⏰ Time & Schedule")

        # ===== PRODUCTIVITY TAB =====
        prod_widget = QWidget()
        prod_layout = QVBoxLayout(prod_widget)
        prod_form = QFormLayout()

        self.pomodoro_spin = QSpinBox()
        self.pomodoro_spin.setRange(5, 120)
        self.pomodoro_spin.setValue(self.settings.get("pomodoro_duration", 25))
        self.pomodoro_spin.setSuffix(" min")

        self.break_spin = QSpinBox()
        self.break_spin.setRange(1, 30)
        self.break_spin.setValue(self.settings.get("break_duration", 5))
        self.break_spin.setSuffix(" min")

        self.goal_hours_spin = QSpinBox()
        self.goal_hours_spin.setRange(5, 100)
        self.goal_hours_spin.setValue(self.settings.get("weekly_goal_hours", 40))
        self.goal_hours_spin.setSuffix(" hours")

        prod_form.addRow("Pomodoro Duration", self.pomodoro_spin)
        prod_form.addRow("Break Duration", self.break_spin)
        prod_form.addRow("Weekly Goal", self.goal_hours_spin)
        
        prod_layout.addLayout(prod_form)
        prod_layout.addStretch()
        
        tabs.addTab(prod_widget, "🎯 Productivity")

        # ===== DISPLAY TAB =====
        display_widget = QWidget()
        display_layout = QVBoxLayout(display_widget)
        display_form = QFormLayout()

        self.font_combo = QComboBox()
        self.font_combo.addItems(["Small", "Medium", "Large"])
        self.font_combo.setCurrentText(self.settings.get("font_size", "Medium"))

        self.always_top_combo = QComboBox()
        self.always_top_combo.addItems(["No", "Yes"])
        self.always_top_combo.setCurrentText("Yes" if self.settings.get("always_on_top", False) else "No")

        self.notif_pos_combo = QComboBox()
        self.notif_pos_combo.addItems(["top-left", "top-right", "bottom-left", "bottom-right"])
        self.notif_pos_combo.setCurrentText(self.settings.get("notification_position", "bottom-right"))

        display_form.addRow("Font Size", self.font_combo)
        display_form.addRow("Always on Top", self.always_top_combo)
        display_form.addRow("Notification Position", self.notif_pos_combo)
        
        display_layout.addLayout(display_form)
        display_layout.addStretch()
        
        tabs.addTab(display_widget, "📺 Display")

        # ===== BACKGROUNDS TAB =====
        bg_widget = QWidget()
        bg_layout = QVBoxLayout(bg_widget)
        
        bg_title = QLabel("🖼️ Select Background")
        bg_title.setStyleSheet("font-weight: bold; font-size: 12px; color: #00FF9C;")
        bg_layout.addWidget(bg_title)
        
        self.bg_list = QListWidget()
        self.bg_list.setStyleSheet("""
            QListWidget { background-color: #08111E; border: 1px solid #1E293B; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #1E293B; }
            QListWidget::item:hover { background-color: #111B30; }
            QListWidget::item:selected { background-color: #00FF9C; color: #05080F; }
        """)
        self.bg_list.itemSelectionChanged.connect(self.on_bg_selected)
        bg_layout.addWidget(self.bg_list)
        
        # Preview
        self.bg_preview = QLabel("Preview")
        self.bg_preview.setStyleSheet("border: 1px solid #1E293B; border-radius: 6px; padding: 20px; min-height: 100px; background-color: #0B1220;")
        self.bg_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bg_layout.addWidget(self.bg_preview)
        
        # Load button
        load_bg_btn = QPushButton("📂 Load Custom Background")
        load_bg_btn.clicked.connect(self.load_custom_background)
        bg_layout.addWidget(load_bg_btn)
        
        # Populate backgrounds
        self.populate_backgrounds()
        
        tabs.addTab(bg_widget, "🖼️ Backgrounds")

        # ===== DATA TAB =====
        data_widget = QWidget()
        data_layout = QVBoxLayout(data_widget)
        data_form = QFormLayout()

        self.backup_combo = QComboBox()
        self.backup_combo.addItems(["Disabled", "Enabled"])
        self.backup_combo.setCurrentText("Enabled" if self.settings.get("auto_backup_enabled", True) else "Disabled")

        self.backup_freq_combo = QComboBox()
        self.backup_freq_combo.addItems(["daily", "weekly", "monthly"])
        self.backup_freq_combo.setCurrentText(self.settings.get("auto_backup_frequency", "daily"))

        data_form.addRow("Auto-backup", self.backup_combo)
        data_form.addRow("Backup Frequency", self.backup_freq_combo)
        
        data_layout.addLayout(data_form)
        
        # Backup buttons
        backup_btn = QPushButton("💾 Backup Now")
        backup_btn.clicked.connect(self.do_backup)
        data_layout.addWidget(backup_btn)
        
        data_layout.addStretch()
        
        tabs.addTab(data_widget, "💾 Data")

        layout.addWidget(tabs)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def on_theme_changed(self):
        theme_name = self.theme_combo.currentText()
        colors = get_theme_colors(theme_name)
        preview = f"""
        <div style='color: {colors['text']}; background: {colors['bg']};'>
        <b>{theme_name}</b><br>
        Accent: <b style='color: {colors['accent']};'>█ {colors['accent']}</b><br>
        Secondary: <b style='color: {colors['secondary']};'>█ {colors['secondary']}</b><br>
        Danger: <b style='color: {colors['danger']};'>█ {colors['danger']}</b>
        </div>
        """
        self.theme_preview.setText(preview)

    def get_settings(self):
        return {
            "discord_webhook_url": self.webhook_input.text().strip(),
            "reminders_enabled": self.reminders_combo.currentText() == "Enabled",
            "tray_notifications_enabled": self.tray_combo.currentText() == "Enabled",
            "sound_alerts_enabled": self.sound_combo.currentText() == "Enabled",
            "theme_name": self.theme_combo.currentText(),
            "work_hours_enabled": self.work_hours_check.currentText() == "Enabled",
            "work_start_hour": self.work_start.time().hour(),
            "work_end_hour": self.work_end.time().hour(),
            "pomodoro_duration": self.pomodoro_spin.value(),
            "break_duration": self.break_spin.value(),
            "font_size": self.font_combo.currentText(),
            "weekly_goal_hours": self.goal_hours_spin.value(),
            "auto_backup_enabled": self.backup_combo.currentText() == "Enabled",
            "auto_backup_frequency": self.backup_freq_combo.currentText(),
            "always_on_top": self.always_top_combo.currentText() == "Yes",
            "notification_position": self.notif_pos_combo.currentText(),
            "background_file": self.selected_bg,
        }

    def populate_backgrounds(self):
        """Load available backgrounds"""
        bg_dir = self.get_backgrounds_folder()
        self.bg_list.clear()
        self.selected_bg = self.settings.get("background_file", "")
        
        # Add "None" option
        item = QListWidgetItem("➖ None (Dark Background)")
        item.setData(Qt.ItemDataRole.UserRole, "")
        self.bg_list.addItem(item)
        
        # Scan for images
        try:
            if os.path.exists(bg_dir):
                files = sorted(os.listdir(bg_dir))
                for file in files:
                    if file.lower().endswith(('.gif', '.png', '.jpg', '.jpeg', '.bmp')):
                        path = os.path.join(bg_dir, file)
                        # Use icon to show preview
                        item = QListWidgetItem(f"🖼️ {file}")
                        item.setData(Qt.ItemDataRole.UserRole, path)
                        self.bg_list.addItem(item)
                        
                        if path == self.selected_bg:
                            self.bg_list.setCurrentItem(item)
            
            # If nothing selected yet, select "None"
            if self.bg_list.currentRow() == -1:
                self.bg_list.setCurrentRow(0)
            
            # Explicitly call on_bg_selected to update preview
            self.on_bg_selected()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load backgrounds: {str(e)}")

    def get_backgrounds_folder(self) -> str:
        """Get backgrounds folder, create if needed"""
        if hasattr(sys, "_MEIPASS"):
            bg_path = os.path.expanduser("~/.cyber-planner/backgrounds")
        else:
            bg_path = os.path.join(os.getcwd(), "backgrounds")
        
        os.makedirs(bg_path, exist_ok=True)
        return bg_path

    def on_bg_selected(self):
        """Handle background selection"""
        item = self.bg_list.currentItem()
        if item:
            self.selected_bg = item.data(Qt.ItemDataRole.UserRole) or ""
            filename = os.path.basename(self.selected_bg) if self.selected_bg else "None"
            
            # Try to load image preview
            if self.selected_bg and os.path.exists(self.selected_bg):
                try:
                    pixmap = QPixmap(self.selected_bg)
                    if not pixmap.isNull():
                        # Scale to fit preview area
                        scaled = pixmap.scaledToWidth(450, Qt.TransformationMode.SmoothTransformation)
                        self.bg_preview.setPixmap(scaled)
                    else:
                        self.bg_preview.setText(f"✓ Selected: {filename}\n(Preview unavailable)")
                except Exception as e:
                    self.bg_preview.setText(f"✓ Selected: {filename}\n(Preview failed)")
            else:
                self.bg_preview.setText("✓ Selected: None (Dark Background)")

    def load_custom_background(self):
        """Open file dialog to select background"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Background Image",
            "",
            "Images (*.png *.jpg *.jpeg *.gif);;All Files (*)"
        )
        
        if file_path:
            bg_dir = self.get_backgrounds_folder()
            filename = os.path.basename(file_path)
            dest_path = os.path.join(bg_dir, filename)
            
            # Copy file to backgrounds folder
            try:
                import shutil
                shutil.copy2(file_path, dest_path)
                self.populate_backgrounds()
                self.show_tray_message("✓ Background Added", f"Added: {filename}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to copy background: {str(e)}")

    def do_backup(self):
        """Create backup of current data"""
        if not self.storage:
            QMessageBox.warning(self, "Error", "Storage not available")
            return
        
        backup_dir = os.path.expanduser("~/.cyber-planner/backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.json")
        
        try:
            backup_data = {
                "tasks": self.storage.tasks,
                "settings": self.storage.settings,
            }
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=4)
            
            QMessageBox.information(self, "✓ Backup Complete", f"Saved to:\n{backup_file}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Backup failed: {str(e)}")

    def show_tray_message(self, title: str, message: str):
        """Show tray message (stub - would be called from main window)"""
        QMessageBox.information(self, title, message)


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
        self.current_quote_index = 0  # For rotating quotes

        # Update window title
        window_title = f"{APP_NAME} v2.5"
        self.setWindowTitle(window_title)
        self.setWindowIcon(self.app_icon)
        self.resize(1350, 750)
        self.setMinimumSize(QSize(700, 450))  # Prevent window from being too small

        self._build_ui()
        self.load_background()
        self._build_tray()
        self.apply_dark_theme()
        self.refresh_calendar()
        self.refresh_task_list()
        self.refresh_analytics()
        self.refresh_dashboard_advanced()  # Advanced dashboard with suggestions and burndown
        self.refresh_habits()
        self.refresh_heatmap()

        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(30000)

        # Timer for updating real-time widgets (clock, stats, etc.)
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_realtime_widgets)
        self.update_timer.start(1000)  # Update every second

        self.check_reminders()
        self.show_todays_agenda()
        self.update_realtime_widgets()  # Initial update

    def load_background(self):
        try:
            # Get central widget
            central = self.centralWidget()
            if not central:
                return

            # Clean up old background first
            if hasattr(self, "bg_label") and self.bg_label:
                try:
                    if hasattr(self, "bg_movie"):
                        self.bg_movie.stop()
                    self.bg_label.deleteLater()
                except Exception:
                    pass

            # Get background file
            bg_file = self.storage.settings.get("background_file", "").strip()

            # If no background file is set, use default
            if not bg_file or bg_file == "":
                bg_file = resource_path("200.gif")
            
            # If file doesn't exist, try bundled version
            if not os.path.exists(bg_file):
                print(f"[DEBUG] Background not found: {bg_file}, trying default...")
                bg_file = resource_path("200.gif")
            
            # If still doesn't exist, give up gracefully
            if not os.path.exists(bg_file):
                print(f"[DEBUG] Default background not found either: {bg_file}")
                return

            print(f"[DEBUG] Loading background: {bg_file}")

            # Create background label BEFORE raising other widgets to ensure it's behind
            self.bg_label = QLabel(central)
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
            self.bg_label.setScaledContents(True)
            self.bg_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            # Exclude from layout management
            self.bg_label.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect, False)

            # Load GIF or static image
            if bg_file.lower().endswith(".gif"):
                self.bg_movie = QMovie(bg_file)
                if self.bg_movie.isValid() and self.bg_movie.frameCount() > 0:
                    self.bg_label.setMovie(self.bg_movie)
                    self.bg_movie.start()
                    print(f"[DEBUG] Loaded GIF: {bg_file} ({self.bg_movie.frameCount()} frames)")
                else:
                    # Fallback to static image if GIF is invalid
                    pixmap = QPixmap(bg_file)
                    if not pixmap.isNull():
                        self.bg_label.setPixmap(pixmap)
                        print(f"[DEBUG] Loaded GIF as static image: {bg_file}")
                    else:
                        print(f"[DEBUG] Failed to load GIF: {bg_file}")
                        self.bg_label.deleteLater()
                        return
            else:
                # Load static image (PNG, JPG, etc.)
                pixmap = QPixmap(bg_file)
                if not pixmap.isNull():
                    self.bg_label.setPixmap(pixmap)
                    print(f"[DEBUG] Loaded static image: {bg_file}")
                else:
                    print(f"[DEBUG] Failed to load image: {bg_file}")
                    self.bg_label.deleteLater()
                    return

            # Force stacking order: background at bottom, all other widgets on top
            self.bg_label.lower()
            self.bg_label.show()
            
            # Then raise ALL other widgets explicitly (only widgets, not layouts)
            for child in central.children():
                if child is not self.bg_label and isinstance(child, QWidget):
                    child.raise_()
            
            print(f"[DEBUG] Background stacked: label is behind all UI elements")
            
        except Exception as e:
            print(f"[DEBUG] Error loading background: {str(e)}")
            import traceback
            traceback.print_exc()

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

        self.menu_btn = QPushButton("≡ Menu")
        self.menu_btn.clicked.connect(self.show_menu)

        header.addWidget(self.prev_btn)
        header.addWidget(self.today_btn)
        header.addWidget(self.month_label, 1)
        header.addWidget(self.settings_btn)
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

        # ============= SIDEBAR (RIGHT PANEL) =============
        right_panel = QWidget()
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.setContentsMargins(0, 0, 0, 0)
        right_panel_layout.setSpacing(0)
        
        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical { width: 8px; background-color: #0B1220; }
            QScrollBar::handle:vertical { background-color: #00FF9C; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background-color: #00E066; }
        """)
        
        scroll_widget = QWidget()
        right_layout = QVBoxLayout(scroll_widget)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(12)

        # USER PROFILE SECTION
        profile_group = QGroupBox("👤 Profile")
        profile_group.setStyleSheet("""
            QGroupBox {
                background-color: #0F172A;
                border: 2px solid #00FF9C;
                border-radius: 10px;
                padding-top: 15px;
                margin-top: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                color: #00FF9C;
                font-weight: bold;
            }
        """)
        profile_layout = QVBoxLayout(profile_group)
        profile_layout.setSpacing(8)
        profile_layout.setContentsMargins(10, 10, 10, 10)
        
        app_status = QLabel("✓ Application Ready")
        app_status.setStyleSheet("color: #00FF9C; font-weight: bold; font-size: 11px;")
        profile_layout.addWidget(app_status)
        profile_layout.addStretch()
        
        right_layout.addWidget(profile_group)

        # QUICK STATS SECTION
        stats_group = QGroupBox("📊 Quick Stats")
        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(6)
        stats_layout.setContentsMargins(10, 10, 10, 10)
        
        self.today_count_label = QLabel("📅 Today: 0")
        self.today_count_label.setStyleSheet("color: #7DD3FC; font-size: 11px; font-weight: bold;")
        self.week_count_label = QLabel("📆 Week: 0")
        self.week_count_label.setStyleSheet("color: #86EFAC; font-size: 11px; font-weight: bold;")
        self.total_count_label = QLabel("📋 Total: 0")
        self.total_count_label.setStyleSheet("color: #FCA5A5; font-size: 11px; font-weight: bold;")
        
        stats_layout.addWidget(self.today_count_label)
        stats_layout.addWidget(self.week_count_label)
        stats_layout.addWidget(self.total_count_label)
        right_layout.addWidget(stats_group)

        # DATE & NAVIGATION SECTION
        date_group = QGroupBox("📅 Selected Date")
        date_layout = QVBoxLayout(date_group)
        date_layout.setSpacing(8)
        date_layout.setContentsMargins(10, 10, 10, 10)
        
        self.selected_label = QLabel()
        self.selected_label.setObjectName("SelectedDateLabel")
        self.selected_label.setStyleSheet("color: #00FF9C; font-weight: bold; font-size: 12px;")
        self.selected_label.setWordWrap(True)
        date_layout.addWidget(self.selected_label)
        
        date_nav_layout = QHBoxLayout()
        date_prev = QPushButton("◀")
        date_prev.setMaximumWidth(40)
        date_prev.clicked.connect(self.prev_date)
        date_today = QPushButton("Today")
        date_today.clicked.connect(self.go_today)
        date_next = QPushButton("▶")
        date_next.setMaximumWidth(40)
        date_next.clicked.connect(self.next_date)
        
        date_nav_layout.addWidget(date_prev)
        date_nav_layout.addWidget(date_today, 1)
        date_nav_layout.addWidget(date_next)
        date_layout.addLayout(date_nav_layout)
        right_layout.addWidget(date_group)

        # QUICK ACTIONS SECTION
        action_group = QGroupBox("⚡ Quick Actions")
        action_layout = QVBoxLayout(action_group)
        action_layout.setSpacing(8)
        action_layout.setContentsMargins(10, 10, 10, 10)
        
        self.add_task_btn = QPushButton("➕ New Task")
        self.add_task_btn.clicked.connect(self.open_add_task_dialog)
        self.add_task_btn.setMinimumHeight(36)
        self.add_task_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #003D26, stop:1 #005A3F);
                color: #00FF9C;
                border: 1px solid #00FF9C;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #004D33, stop:1 #007A4F);
                border: 2px solid #00FF9C;
            }
        """)
        
        quick_btns = QHBoxLayout()
        quick_btns.setSpacing(6)
        snooze_btn = QPushButton("⏰ Snooze")
        snooze_btn.clicked.connect(self.snooze_task)
        snooze_btn.setMinimumHeight(32)
        snooze_btn.setStyleSheet("font-size: 10px; padding: 6px; font-weight: bold;")
        pomodoro_btn = QPushButton("🍅 Pomo")
        pomodoro_btn.clicked.connect(self.start_pomodoro)
        pomodoro_btn.setMinimumHeight(32)
        pomodoro_btn.setStyleSheet("font-size: 10px; padding: 6px; font-weight: bold;")
        quick_btns.addWidget(snooze_btn)
        quick_btns.addWidget(pomodoro_btn)
        
        action_layout.addWidget(self.add_task_btn)
        action_layout.addLayout(quick_btns)
        right_layout.addWidget(action_group)

        # FILTERING & SORTING SECTION
        filter_group = QGroupBox("🔍 Filter & Sort")
        filter_layout = QVBoxLayout(filter_group)
        filter_layout.setSpacing(8)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        
        search_label = QLabel("Search:")
        search_label.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: bold;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tasks...")
        self.search_input.setMinimumHeight(28)
        self.search_input.setStyleSheet("font-size: 11px; padding: 4px;")
        self.search_input.textChanged.connect(self.on_search_changed)
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input)

        sort_label = QLabel("Sort:")
        sort_label.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: bold;")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Time", "Duration", "Category", "Priority"])
        self.sort_combo.setMinimumHeight(28)
        self.sort_combo.setStyleSheet("font-size: 10px; padding: 4px;")
        self.sort_combo.currentTextChanged.connect(self.on_sort_changed)
        filter_layout.addWidget(sort_label)
        filter_layout.addWidget(self.sort_combo)
        
        right_layout.addWidget(filter_group)

        # CATEGORY SHORTCUTS
        category_group = QGroupBox("🏷️ Categories")
        category_layout = QVBoxLayout(category_group)
        category_layout.setSpacing(6)
        category_layout.setContentsMargins(10, 10, 10, 10)
        
        self.category_buttons = {}
        categories = ["Work", "Personal", "Urgent", "Coding", "Health"]
        category_btn_grid = QGridLayout()
        category_btn_grid.setSpacing(5)
        category_btn_grid.setContentsMargins(0, 0, 0, 0)
        
        for idx, cat in enumerate(categories):
            cat_btn = QPushButton(cat)
            cat_btn.setMinimumHeight(32)
            cat_color = CATEGORY_COLORS.get(cat, "#6B7280")
            cat_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {CATEGORY_BG.get(cat, '#111827')};
                    color: {cat_color};
                    border: 1px solid {cat_color};
                    border-radius: 6px;
                    padding: 6px;
                    font-size: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    border: 2px solid {cat_color};
                    background-color: {CATEGORY_BG.get(cat, '#111827')};
                    color: #FFFFFF;
                }}
            """)
            self.category_buttons[cat] = cat_btn
            row = idx // 2
            col = idx % 2
            category_btn_grid.addWidget(cat_btn, row, col)
        
        category_layout.addLayout(category_btn_grid)
        right_layout.addWidget(category_group)

        # ============= REAL-TIME STATS SECTION =============
        realtime_group = QGroupBox("⏰ Real-Time Stats")
        realtime_layout = QVBoxLayout(realtime_group)
        realtime_layout.setSpacing(8)
        realtime_layout.setContentsMargins(10, 10, 10, 10)
        
        # Digital Clock
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setStyleSheet("color: #00FF9C; font-size: 18px; font-weight: bold; text-align: center;")
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        realtime_layout.addWidget(self.clock_label)
        
        # Weather Widget
        self.weather_label = QLabel("🌤️ Loading weather...")
        self.weather_label.setStyleSheet("color: #7DD3FC; font-size: 10px; font-weight: bold;")
        realtime_layout.addWidget(self.weather_label)
        
        # Completed Tasks Counter
        self.completed_label = QLabel("✓ Completed: 0/0")
        self.completed_label.setStyleSheet("color: #86EFAC; font-size: 11px; font-weight: bold;")
        realtime_layout.addWidget(self.completed_label)
        
        # Time Spent Tracker
        self.time_spent_label = QLabel("⏱️ Today: 0h of planned")
        self.time_spent_label.setStyleSheet("color: #FCA5A5; font-size: 11px; font-weight: bold;")
        realtime_layout.addWidget(self.time_spent_label)
        
        right_layout.addWidget(realtime_group)

        # ============= DAILY MOTIVATION SECTION =============
        motivation_group = QGroupBox("✨ Daily Motivation")
        motivation_layout = QVBoxLayout(motivation_group)
        motivation_layout.setSpacing(8)
        motivation_layout.setContentsMargins(10, 10, 10, 10)
        
        self.quote_label = QLabel(MOTIVATIONAL_QUOTES[0])
        self.quote_label.setStyleSheet("color: #FCA5A5; font-size: 10px; font-weight: bold; font-style: italic;")
        self.quote_label.setWordWrap(True)
        self.quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        motivation_layout.addWidget(self.quote_label)
        
        next_quote_btn = QPushButton("Next Quote →")
        next_quote_btn.setMinimumHeight(28)
        next_quote_btn.setStyleSheet("font-size: 9px; padding: 4px; font-weight: bold;")
        next_quote_btn.clicked.connect(self.show_next_quote)
        motivation_layout.addWidget(next_quote_btn)
        
        right_layout.addWidget(motivation_group)

        # HINTS
        self.complete_hint = QLabel("💡 N=New • Del=Delete • Right-click=Edit")
        self.complete_hint.setStyleSheet("color: #475569; font-size: 9px;")
        self.complete_hint.setWordWrap(True)
        right_layout.addWidget(self.complete_hint)

        right_layout.addSpacing(10)
        right_layout.addStretch()
        
        # Add scrollable content to scroll area
        scroll_area.setWidget(scroll_widget)
        right_panel_layout.addWidget(scroll_area)

        # Create tabbed views (tasks section)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #0F172A;
                color: #D7E3F4;
                padding: 8px 16px;
                border: 1px solid #1E293B;
                border-radius: 6px 6px 0 0;
                margin-right: 2px;
                font-size: 11px;
            }
            QTabBar::tab:selected {
                background-color: #08111E;
                border: 2px solid #00FF9C;
                color: #00FF9C;
            }
            QTabBar::tab:hover:!selected {
                background-color: #111B30;
            }
            QTabWidget::pane {
                border: 1px solid #1E293B;
                background-color: #08111E;
            }
        """)

        # Tab 1: Today
        today_widget = QWidget()
        today_layout = QVBoxLayout(today_widget)
        self.today_task_list = DraggableTaskList(main_window=self)
        self.today_task_list.itemChanged.connect(self.handle_task_checked)
        today_layout.addWidget(self.today_task_list)
        self.tabs.addTab(today_widget, "📅 Today")

        # Tab 2: This Week
        week_widget = QWidget()
        week_layout = QVBoxLayout(week_widget)
        self.week_task_list = DraggableTaskList(main_window=self)
        self.week_task_list.itemChanged.connect(self.handle_task_checked)
        week_layout.addWidget(self.week_task_list)
        self.tabs.addTab(week_widget, "📆 This Week")

        # Tab 3: All Tasks
        all_widget = QWidget()
        all_layout = QVBoxLayout(all_widget)
        self.all_task_list = DraggableTaskList(main_window=self)
        self.all_task_list.itemChanged.connect(self.handle_task_checked)
        all_layout.addWidget(self.all_task_list)
        self.tabs.addTab(all_widget, "📋 All Tasks")

        # Tab 4: Dashboard
        dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_widget)
        dashboard_scroll = QScrollArea()
        dashboard_scroll.setWidgetResizable(True)
        dashboard_content = QWidget()
        self.dashboard_layout = QVBoxLayout(dashboard_content)
        dashboard_scroll.setWidget(dashboard_content)
        dashboard_layout.addWidget(dashboard_scroll)
        self.tabs.addTab(dashboard_widget, "📊 Dashboard")

        # Tab 5: Habits
        habits_widget = QWidget()
        habits_layout = QVBoxLayout(habits_widget)
        habits_top = QHBoxLayout()
        habits_title = QLabel("🎯 Daily Habits")
        habits_title.setStyleSheet("font-weight: bold; font-size: 12px; color: #00FF9C;")
        habits_add_btn = QPushButton("+ Add Habit")
        habits_add_btn.setMaximumWidth(100)
        habits_add_btn.clicked.connect(self.open_add_habit_dialog)
        habits_top.addWidget(habits_title)
        habits_top.addStretch()
        habits_top.addWidget(habits_add_btn)
        habits_layout.addLayout(habits_top)
        
        self.habits_list = QListWidget()
        self.habits_list.setStyleSheet("""
            QListWidget { background-color: #08111E; border: 1px solid #1E293B; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #1E293B; }
            QListWidget::item:hover { background-color: #111B30; }
        """)
        habits_layout.addWidget(self.habits_list)
        self.tabs.addTab(habits_widget, "🎯 Habits")

        # Tab 6: Heatmap
        heatmap_widget = QWidget()
        heatmap_layout = QVBoxLayout(heatmap_widget)
        heatmap_title = QLabel("🔥 Productivity Heatmap")
        heatmap_title.setStyleSheet("font-weight: bold; font-size: 12px; color: #00FF9C;")
        heatmap_layout.addWidget(heatmap_title)
        
        self.heatmap_area = QLabel()
        self.heatmap_area.setStyleSheet("background-color: #08111E; padding: 20px; border-radius: 8px;")
        self.heatmap_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.heatmap_area.setMinimumHeight(300)
        self.heatmap_area.setWordWrap(True)
        heatmap_layout.addWidget(self.heatmap_area)
        heatmap_layout.addStretch()
        self.tabs.addTab(heatmap_widget, "🔥 Heatmap")

        right_panel_layout.addWidget(self.tabs, 1)

        splitter.addWidget(right_panel)
        splitter.setSizes([750, 600])
        root.addWidget(splitter)

        # Create Floating Action Button
        self.fab = QPushButton("+")
        self.fab.setFixedSize(60, 60)
        self.fab.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.fab.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fab.clicked.connect(self.open_add_task_dialog)
        self.fab.setStyleSheet("""
            QPushButton {
                background-color: #00FF9C;
                color: #05080F;
                border: 2px solid #00FF9C;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #00E066;
                border: 2px solid #00E066;
            }
            QPushButton:pressed {
                background-color: #00CC52;
                border: 2px solid #00CC52;
            }
        """)
        self.fab_position_update_timer = QTimer()
        self.fab_position_update_timer.timeout.connect(self.update_fab_position)
        self.fab_position_update_timer.start(100)

    def change_background(self):
        """Change background - delegates to safe version for exe compatibility"""
        self.change_background_safe()

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
                "╔════════════════════════════════════════════════════════════╗\n"
                "║          CYBER PLANNER v2.5 - ADVANCED EDITION             ║\n"
                "║       Intelligent Task Management & Productivity System     ║\n"
                "╚════════════════════════════════════════════════════════════╝\n\n"
                "A powerful, dark-themed task management application built with PyQt6\n"
                "for maximum productivity and intelligent workflow optimization.\n\n"
                "✨ CORE FEATURES:\n"
                "  ✓ Full interactive calendar with month navigation\n"
                "  ✓ Intelligent task creation with priorities & recurring options\n"
                "  ✓ Task completion tracking with timestamps\n"
                "  ✓ Multi-profile & multi-user support with authentication\n"
                "  ✓ Drag-and-drop tasks between dates\n"
                "  ✓ CSV import/export for data portability\n"
                "  ✓ Custom backgrounds (static images & animated GIFs)\n"
                "  ✓ System tray integration with notifications\n\n"
                "⏰ PRODUCTIVITY TOOLS:\n"
                "  ✓ Pomodoro timer (25-minute focus sessions)\n"
                "  ✓ Smart task reminders (15min, 5min, at-time)\n"
                "  ✓ Digital clock with real-time weather indicator\n"
                "  ✓ Focus mode toggle for distraction-free deep work\n"
                "  ✓ Completion time tracker & analytics\n\n"
                "📊 ANALYTICS & INSIGHTS:\n"
                "  ✓ Weekly productivity dashboard with comprehensive stats\n"
                "  ✓ Completion rate tracking by category & day\n"
                "  ✓ Time spent analysis (planned vs completed)\n"
                "  ✓ Task status tracking (Not Started/In Progress/Completed)\n"
                "  ✓ Energy level assessment (Low/Medium/High)\n"
                "  ✓ Category-based workload distribution\n\n"
                "🔧 INTEGRATION & AUTOMATION:\n"
                "  ✓ Discord webhook notifications\n"
                "  ✓ Search & filter tasks in real-time\n"
                "  ✓ Sort by Time, Duration, Category, or Priority\n"
                "  ✓ Category quick-access shortcuts\n"
                "  ✓ Task duplication & quick snooze\n"
                "  ✓ Settings persistence (per-profile)\n\n"
                "⌨️  KEYBOARD SHORTCUTS:\n"
                "  N - Create new task\n"
                "  Del - Delete selected task\n"
                "  Right-click - Task context menu (Edit/Duplicate/Delete)\n\n"
                "💡 DAILY MOTIVATION:\n"
                "  ✓ 15 rotating motivational quotes\n"
                "  ✓ Real-time task statistics\n"
                "  ✓ Progress visualization\n\n"
                "🛡️  SECURITY & DATA:\n"
                "  ✓ User authentication with password hashing (SHA256)\n"
                "  ✓ Per-user profile isolation\n"
                "  ✓ Local JSON-based persistent storage\n"
                "  ✓ EXE build support with file relocation\n\n"
                "👨‍💻 CREATED BY:\n"
                "  galmx (xdrew87)\n"
                "  GitHub: github.com/xdrew87\n\n"
                "📝 LICENSE:\n"
                "  © 2026 - All rights reserved.\n"
                "  For custom use and licensing inquiries.",
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
        if hasattr(self, "bg_label") and self.bg_label:
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
            # Re-raise UI elements to stay on top (only widgets, not layouts)
            central = self.centralWidget()
            if central:
                for child in central.children():
                    if child is not self.bg_label and isinstance(child, QWidget):
                        child.raise_()
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
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 12px;
                padding-left: 8px;
                padding-right: 8px;
                padding-bottom: 8px;
                background-color: #0A1520;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
                color: #00FF9C;
                font-weight: bold;
                font-size: 10px;
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
        task_date = item.data(Qt.ItemDataRole.UserRole + 1)
        task = None
        for t in self.storage.get_tasks_for_date(task_date):
            if t["id"] == task_id:
                task = t
                break

        if not task:
            return

        categories = self.storage.settings.get("custom_categories", ["Work", "Personal", "Urgent", "Coding"])
        dialog = AddTaskDialog(self, task_date, task, categories)
        if dialog.exec():
            updated_task = dialog.get_task()
            self.storage.update_task(task_date, updated_task)
            self.refresh_task_list()
            self.refresh_calendar()
            self.refresh_analytics()

    def duplicate_task(self, item: QListWidgetItem):
        try:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            task_date = item.data(Qt.ItemDataRole.UserRole + 1)
            task = None
            for t in self.storage.get_tasks_for_date(task_date):
                if t["id"] == task_id:
                    task = t.copy()
                    break

            if not task:
                QMessageBox.warning(self, "Error", "Task not found.")
                return

            task["id"] = str(uuid.uuid4())
            task["created_at"] = datetime.now().isoformat()
            task["reminders_sent"] = []
            self.storage.add_task(task_date, task)
            self.refresh_task_list()
            self.refresh_calendar()
            self.refresh_analytics()
            QMessageBox.information(self, "Duplicated", f"Task '{task['title']}' duplicated.")
        except Exception as e:
            QMessageBox.critical(self, "Duplicate Error", f"Failed to duplicate task: {str(e)}")

    def delete_task_from_menu(self, item: QListWidgetItem):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        task_date = item.data(Qt.ItemDataRole.UserRole + 1)
        
        reply = QMessageBox.question(self, "Delete", "Delete this task?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.storage.delete_task(task_date, task_id)
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

        dialog = SettingsDialog(self, settings_copy, self.storage)
        if dialog.exec():
            updated = dialog.get_settings()
            self.storage.settings.update(updated)
            self.storage.save_settings()
            
            # Apply settings changes
            self.apply_settings_changes(updated)
            
            QMessageBox.information(self, "✓ Saved", "Settings updated successfully!")

    def apply_settings_changes(self, settings: dict):
        """Apply non-persistent UI settings"""
        # Apply always-on-top
        if settings.get("always_on_top", False):
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
            self.show()
        
        # Apply font size
        font_size = settings.get("font_size", "Medium")
        scale = {"Small": 10, "Medium": 11, "Large": 13}.get(font_size, 11)
        font = QFont("Arial", scale)
        QApplication.instance().setFont(font)
        
        # Load new background if changed (reload even if empty to apply "None")
        if "background_file" in settings:
            self.load_background()


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
        
        # Get selected date info
        selected_dt = parse_date_key(self.selected_date)
        self.selected_label.setText(f"Tasks for {selected_dt.strftime('%A, %B %d, %Y')}")

        # REFRESH TODAY TAB
        self.today_task_list.clear()
        today_tasks = list(self.storage.get_tasks_for_date(self.selected_date))
        self._populate_task_list(self.today_task_list, today_tasks, self.selected_date)

        # REFRESH THIS WEEK TAB
        self.week_task_list.clear()
        week_start, week_end = self.get_week_range(selected_dt)
        week_tasks = []
        current = week_start
        while current <= week_end:
            ds = date_key(current)
            week_tasks.extend(self.storage.get_tasks_for_date(ds))
            current += timedelta(days=1)
        self._populate_task_list(self.week_task_list, week_tasks, self.selected_date, show_dates=True)

        # REFRESH ALL TASKS TAB
        self.all_task_list.clear()
        all_tasks = []
        for date_str, tasks in self.storage.tasks.items():
            all_tasks.extend(tasks)
        self._populate_task_list(self.all_task_list, all_tasks, self.selected_date, show_dates=True)

        # REFRESH DASHBOARD
        self.refresh_dashboard()

        self.loading_tasks = False
        self.update_quick_stats()

    def _populate_task_list(self, task_list: DraggableTaskList, tasks: list, selected_date: str, show_dates: bool = False):
        """Helper to populate a task list widget"""
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
            category = task.get("category", "Work")
            notes_preview = f" | {task.get('notes', '')[:15]}" if task.get('notes') else ""
            
            # Enhanced badges with emojis
            priority_icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            priority_badge = priority_icons.get(priority, "🟡")
            
            recurring_badge = "🔄 " if recurring != "None" else ""
            category_emoji = {
                "Work": "💼",
                "Personal": "👤",
                "Urgent": "⚡",
                "Coding": "💻",
                "Health": "🏥",
                "Finance": "💰",
                "Learning": "📚",
                "Other": "📌",
            }.get(category, "📝")
            
            duration_bar = "▓" * max(1, min(10, duration // 30))
            
            date_part = f"[{task.get('date', selected_date)[:5]}] " if show_dates else ""
            text = f"{task['time']} {duration_bar} {priority_badge} {category_emoji} {duration}m | {recurring_badge}{task['title']}{notes_preview}"
            
            item = QListWidgetItem(text)
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsSelectable
                | Qt.ItemFlag.ItemIsDragEnabled
            )
            item.setCheckState(Qt.CheckState.Unchecked)
            
            # Store task ID and its original date
            task_date = None
            for date_str, date_tasks in self.storage.tasks.items():
                if any(t.get("id") == task.get("id") for t in date_tasks):
                    task_date = date_str
                    break
            
            item.setData(Qt.ItemDataRole.UserRole, task["id"])
            item.setData(Qt.ItemDataRole.UserRole + 1, task_date or selected_date)

            fg = QColor(CATEGORY_COLORS.get(category, "#D7E3F4"))
            bg = QColor(CATEGORY_BG.get(category, "#111827"))
            item.setForeground(fg)
            item.setBackground(bg)

            task_list.addItem(item)

    def refresh_dashboard(self):
        """Refresh the dashboard tab with analytics"""
        # Clear existing dashboard
        while self.dashboard_layout.count():
            item = self.dashboard_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Calculate comprehensive stats
        selected_dt = parse_date_key(self.selected_date)
        week_start, week_end = self.get_week_range(selected_dt)

        total_tasks = 0
        total_minutes = 0
        completed_count = 0
        category_breakdown = {}
        busy_days = {}

        current = week_start
        while current <= week_end:
            ds = date_key(current)
            day_minutes = 0
            for task in self.storage.get_tasks_for_date(ds):
                total_tasks += 1
                mins = int(task.get("duration_minutes", 0))
                total_minutes += mins
                day_minutes += mins

                category = task.get("category", "Work")
                category_breakdown[category] = category_breakdown.get(category, 0) + mins

            if day_minutes > 0:
                busy_days[current.strftime("%A")] = day_minutes

            current += timedelta(days=1)

        # Title
        title = QLabel("📊 PRODUCTIVITY DASHBOARD")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #00FF9C;")
        self.dashboard_layout.addWidget(title)

        # Stats grid
        stats_group = QGroupBox("📈 Weekly Overview")
        stats_layout = QGridLayout(stats_group)

        stat_cards = [
            (f"Total Tasks", f"{total_tasks}", "🎯"),
            (f"Total Time", f"{pretty_hours(total_minutes)}", "⏱️"),
            (f"Completion Rate", f"{(completed_count / max(total_tasks, 1) * 100):.1f}%", "✅"),
            (f"Busiest Day", f"{max(busy_days, key=busy_days.get) if busy_days else 'N/A'}", "🔥"),
        ]

        for idx, (label, value, emoji) in enumerate(stat_cards):
            row = idx // 2
            col = idx % 2

            card = QGroupBox()
            card.setStyleSheet("""
                QGroupBox {
                    border: 2px solid #00FF9C;
                    border-radius: 12px;
                    margin-top: 10px;
                    background-color: #08111E;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 6px;
                    color: #00FF9C;
                    font-weight: bold;
                }
            """)
            card_layout = QVBoxLayout(card)

            card_title = QLabel(f"{emoji} {label}")
            card_title.setStyleSheet("color: #7DD3FC; font-weight: bold;")
            card_layout.addWidget(card_title)

            card_value = QLabel(value)
            card_value_font = QFont()
            card_value_font.setPointSize(20)
            card_value.setFont(card_value_font)
            card_value.setStyleSheet("color: #00FF9C;")
            card_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(card_value)

            stats_layout.addWidget(card, row, col)

        self.dashboard_layout.addWidget(stats_group)

        # Category breakdown
        breakdown_group = QGroupBox("📂 Time by Category")
        breakdown_layout = QVBoxLayout(breakdown_group)

        if category_breakdown:
            for category in sorted(category_breakdown.keys()):
                minutes = category_breakdown[category]
                percentage = (minutes / max(total_minutes, 1)) * 100
                emoji = {
                    "Work": "💼",
                    "Personal": "👤",
                    "Urgent": "⚡",
                    "Coding": "💻",
                    "Health": "🏥",
                    "Finance": "💰",
                    "Learning": "📚",
                    "Other": "📌",
                }.get(category, "📝")

                cat_widget = QWidget()
                cat_layout = QHBoxLayout(cat_widget)

                cat_label = QLabel(f"{emoji} {category}")
                cat_label.setStyleSheet(f"color: {CATEGORY_COLORS.get(category, '#D7E3F4')}; font-weight: bold;")
                cat_label.setFixedWidth(120)

                cat_bar = QLabel("█" * int(percentage / 5))
                cat_bar.setStyleSheet(f"color: {CATEGORY_COLORS.get(category, '#D7E3F4')};")

                cat_time = QLabel(f"{pretty_hours(minutes)} ({percentage:.1f}%)")
                cat_time.setStyleSheet("color: #94A3B8;")
                cat_time.setFixedWidth(100)

                cat_layout.addWidget(cat_label)
                cat_layout.addWidget(cat_bar, 1)
                cat_layout.addWidget(cat_time)

                breakdown_layout.addWidget(cat_widget)
        else:
            no_tasks = QLabel("No tasks scheduled for this week")
            no_tasks.setStyleSheet("color: #94A3B8;")
            breakdown_layout.addWidget(no_tasks)

        self.dashboard_layout.addWidget(breakdown_group)

        # Add stretch to push content to top
        self.dashboard_layout.addStretch()

    def update_fab_position(self):
        """Update FAB position to bottom-right corner"""
        if hasattr(self, 'fab'):
            parent = self.fab.parent()
            if parent:
                x = parent.width() - self.fab.width() - 20
                y = parent.height() - self.fab.height() - 20
                self.fab.move(x, y)

    def open_add_task_dialog(self):
        categories = self.storage.settings.get("custom_categories", ["Work", "Personal", "Urgent", "Coding"])
        dialog = AddTaskDialog(self, self.selected_date, None, categories)
        if dialog.exec():
            task = dialog.get_task()
            self.storage.add_task(self.selected_date, task)
            self.refresh_task_list()
            self.refresh_calendar()
            self.refresh_analytics()
            self.refresh_dashboard_advanced()
            self.refresh_heatmap()

    def handle_task_checked(self, item: QListWidgetItem):
        if self.loading_tasks:
            return

        if item.checkState() == Qt.CheckState.Checked:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            task_date = item.data(Qt.ItemDataRole.UserRole + 1)
            
            task = None
            for t in self.storage.get_tasks_for_date(task_date):
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

            self.storage.delete_task(task_date, task_id)
            self.refresh_task_list()
            self.refresh_calendar()
            self.refresh_analytics()
            self.refresh_dashboard_advanced()
            self.refresh_heatmap()

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

    def get_current_task_list(self):
        """Get the currently active task list based on selected tab"""
        if self.tabs.currentIndex() == 0:
            return self.today_task_list
        elif self.tabs.currentIndex() == 1:
            return self.week_task_list
        elif self.tabs.currentIndex() == 2:
            return self.all_task_list
        else:
            return self.today_task_list  # Default fallback

    def snooze_task(self):
        """Move selected task to tomorrow"""
        task_list = self.get_current_task_list()
        item = task_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Task", "Please select a task to snooze.")
            return

        task_id = item.data(Qt.ItemDataRole.UserRole)
        task_date = item.data(Qt.ItemDataRole.UserRole + 1)
        task = None
        for t in self.storage.get_tasks_for_date(task_date):
            if t["id"] == task_id:
                task = t.copy()
                break

        if not task:
            return

        tomorrow = parse_date_key(task_date) + timedelta(days=1)
        task["id"] = str(uuid.uuid4())
        task["reminders_sent"] = []

        self.storage.add_task(date_key(tomorrow), task)
        self.storage.delete_task(task_date, task_id)
        self.refresh_task_list()
        self.refresh_calendar()
        self.refresh_analytics()
        QMessageBox.information(self, "Snoozed", f"Task moved to tomorrow ({date_key(tomorrow)}).")

    def start_pomodoro(self):
        """Start a 25-minute Pomodoro timer"""
        task_list = self.get_current_task_list()
        item = task_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Task", "Please select a task for Pomodoro.")
            return

        task_title = item.text().split("|")[-1].strip() if "|" in item.text() else item.text()[:30]

        self.pomodoro_dialog = PomodoroDialog(self, task_title)
        self.pomodoro_dialog.exec()

    def prev_date(self):
        """Go to previous day"""
        current_date = parse_date_key(self.selected_date)
        prev_date = current_date - timedelta(days=1)
        self.select_date(date_key(prev_date))

    def next_date(self):
        """Go to next day"""
        current_date = parse_date_key(self.selected_date)
        next_date = current_date + timedelta(days=1)
        self.select_date(date_key(next_date))

    def update_quick_stats(self):
        """Update quick stats in sidebar"""
        # Today count
        today_tasks = self.storage.get_tasks_for_date(self.selected_date)
        self.today_count_label.setText(f"📅 Today: {len(today_tasks)} tasks")

        # This week count
        selected_dt = parse_date_key(self.selected_date)
        week_start, week_end = self.get_week_range(selected_dt)
        week_count = 0
        current = week_start
        while current <= week_end:
            week_count += len(self.storage.get_tasks_for_date(date_key(current)))
            current += timedelta(days=1)
        self.week_count_label.setText(f"📆 This Week: {week_count} tasks")

        # Total count
        total_tasks = sum(len(tasks) for tasks in self.storage.tasks.values())
        self.total_count_label.setText(f"📋 Total: {total_tasks} tasks")

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
        """Analytics are now shown in the Dashboard tab"""
        # This method is kept for compatibility but analytics are
        # displayed in the Dashboard tab instead of the sidebar
        pass

    def update_realtime_widgets(self):
        """Update all real-time widgets (clock, weather, stats, etc.)"""
        self.update_digital_clock()
        self.update_weather()
        self.update_completed_counter()
        self.update_time_spent()

    def update_digital_clock(self):
        """Update the digital clock display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_label.setText(current_time)

    def update_weather(self):
        """Update weather widget (placeholder - can integrate real API later)"""
        # Placeholder: Shows current temperature estimate
        # To use real weather: install 'requests' and use OpenWeatherMap API
        current_hour = datetime.now().hour
        
        # Simple placeholder weather based on time of day
        if 6 <= current_hour < 12:
            weather_text = "☀️ Morning - Clear"
        elif 12 <= current_hour < 18:
            weather_text = "🌤️ Afternoon - Sunny"
        elif 18 <= current_hour < 21:
            weather_text = "🌅 Evening - Partly Cloudy"
        else:
            weather_text = "🌙 Night - Clear"
        
        self.weather_label.setText(weather_text)

    def update_completed_counter(self):
        """Update completed tasks counter for today"""
        today_tasks = self.storage.get_tasks_for_date(date_key(self.today))
        total_today = len(today_tasks)
        # For now, we'll count completed based on a simple heuristic
        # You can enhance this by adding a 'completed' field to tasks
        completed_count = 0
        
        self.completed_label.setText(f"✓ Completed: {completed_count}/{total_today}")

    def update_time_spent(self):
        """Update time spent tracker for today"""
        today_tasks = self.storage.get_tasks_for_date(date_key(self.today))
        
        # Calculate total planned time (in hours)
        total_minutes = sum(task.get("duration_minutes", 0) for task in today_tasks)
        total_hours = total_minutes / 60
        
        # Calculate how many tasks are done (estimated)
        # This is a placeholder - enhance by tracking actual completion
        self.time_spent_label.setText(f"⏱️ Today: {total_hours:.1f}h planned")

    def show_next_quote(self):
        """Cycle to the next motivational quote"""
        self.current_quote_index = (self.current_quote_index + 1) % len(MOTIVATIONAL_QUOTES)
        quote = MOTIVATIONAL_QUOTES[self.current_quote_index]
        self.quote_label.setText(quote)

    def toggle_focus_mode(self):
        """Toggle focus/deep work mode - hide distractions"""
        if not hasattr(self, 'focus_mode_active'):
            self.focus_mode_active = False
        
        self.focus_mode_active = not self.focus_mode_active
        
        if self.focus_mode_active:
            self.scroll_area.setVisible(False)
            self.show_tray_message("🎯 Focus Mode", "Distraction-free mode enabled")
        else:
            self.scroll_area.setVisible(True)
            self.show_tray_message("Focus Mode", "Focus mode disabled")

    def show_productivity_report(self):
        """Show weekly productivity report"""
        stats = self.storage.get_productivity_stats(7)
        report = f"""
        📊 WEEKLY PRODUCTIVITY REPORT
        
        Total Tasks: {stats['total_tasks']}
        Completed: {stats['completed_tasks']}
        Completion Rate: {stats['completion_rate']:.1f}%
        
        By Category:
        """
        for cat, data in stats["by_category"].items():
            rate = (data["completed"] / data["total"] * 100) if data["total"] > 0 else 0
            report += f"\n  {cat}: {data['completed']}/{data['total']} ({rate:.0f}%)"
        
        self.show_tray_message("Productivity Report", f"{stats['completed_tasks']}/{stats['total_tasks']} tasks completed")

    def get_background_path(self) -> str:
        """Get persistent background path for exe builds"""
        if hasattr(sys, "_MEIPASS"):  # Running as exe
            app_data = os.path.expanduser("~/.cyber-planner")
            os.makedirs(app_data, exist_ok=True)
            return os.path.join(app_data, "backgrounds")
        else:
            return "."

    def change_background_safe(self):
        """Safely change background for both script and exe versions"""
        start_dir = self.get_background_path()
        os.makedirs(start_dir, exist_ok=True)
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Background",
            start_dir,
            "Images (*.png *.jpg *.jpeg *.gif)",
        )

        if not file_path:
            return

        # For exe builds, copy the file to app data folder
        if hasattr(sys, "_MEIPASS"):
            import shutil
            bg_dir = self.get_background_path()
            os.makedirs(bg_dir, exist_ok=True)
            filename = os.path.basename(file_path)
            dest_path = os.path.join(bg_dir, filename)
            shutil.copy2(file_path, dest_path)
            self.storage.settings["background_file"] = dest_path
        else:
            self.storage.settings["background_file"] = file_path
        
        self.storage.save_settings()
        self.load_background()

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

    def open_add_habit_dialog(self):
        """Open dialog to add new habit"""
        dialog = HabitDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            habit = dialog.get_habit()
            self.storage.add_habit(habit)
            self.refresh_habits()
            self.show_tray_message("✨ Habit Added", f"New habit: {habit['name']}")

    def refresh_habits(self):
        """Refresh habits list display"""
        self.habits_list.clear()
        self.storage.init_habits()
        habits = self.storage.settings.get("habits", [])
        
        for habit in habits:
            habit_id = habit["id"]
            streak = self.storage.get_habit_streak(habit_id)
            today = date_key(date.today())
            completed_today = today in habit.get("completed_dates", [])
            
            text = f"{'✓' if completed_today else '○'} {habit['name']} | 🔥 {streak}"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, habit_id)
            
            # Color based on strike
            if streak >= 7:
                item.setForeground(QColor("#FFD700"))  # Gold for 7+ day streaks
            elif streak >= 3:
                item.setForeground(QColor("#00FF9C"))  # Cyan for 3+ day streaks
            elif completed_today:
                item.setForeground(QColor("#86EFAC"))  # Green if done today
            else:
                item.setForeground(QColor("#FCA5A5"))  # Red if not done today
            
            self.habits_list.addItem(item)
        
        self.habits_list.itemClicked.connect(self.complete_habit_click)

    def complete_habit_click(self, item: QListWidgetItem):
        """Mark habit as completed when clicked"""
        habit_id = item.data(Qt.ItemDataRole.UserRole)
        if self.storage.complete_habit_today(habit_id):
            self.refresh_habits()
            play_sound("chime")
            self.show_tray_message("🎉 Habit Complete!", f"Great job keeping up with your habit!")

    def refresh_heatmap(self):
        """Generate and display productivity heatmap"""
        heatmap_data = self.storage.get_daily_heatmap_data(30)
        
        # Create a simple text-based heatmap visualization
        html = "<table cellpadding='3' cellspacing='1' style='border-collapse: collapse; font-size: 10px;'>"
        
        day_groups = []
        current_group = []
        for i, (day_key, data) in enumerate(sorted(heatmap_data.items())):
            if i % 7 == 0 and current_group:
                day_groups.append(current_group)
                current_group = []
            current_group.append((day_key, data))
        if current_group:
            day_groups.append(current_group)
        
        # Display weeks
        for week in day_groups:
            html += "<tr>"
            for day_key, data in week:
                rate = data["rate"]
                # Color intensity based on completion rate
                if rate == 0:
                    color = "#0B1220"
                elif rate < 25:
                    color = "#FF6B6B"
                elif rate < 50:
                    color = "#FFA500"
                elif rate < 75:
                    color = "#FFD700"
                else:
                    color = "#00FF9C"
                
                day_label = datetime.strptime(day_key, "%Y-%m-%d").strftime("%m/%d")
                html += f"<td style='background: {color}; border: 1px solid #1E293B; padding: 8px; width: 40px; text-align: center;' title='{data['completed']}/{data['total']} tasks'>{day_label}</td>"
            html += "</tr>"
        
        html += "</table><p style='font-size: 9px; color: #94A3B8; margin-top: 12px;'>Darker green = Higher completion rate | Red = No tasks</p>"
        self.heatmap_area.setText(html)

    def refresh_dashboard_advanced(self):
        """Enhanced dashboard with burndown chart and visualizations"""
        # Clear existing widgets
        while self.dashboard_layout.count():
            widget = self.dashboard_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        
        # Smart Suggestions
        suggestions = self.storage.get_smart_suggestions()
        if suggestions:
            suggestions_group = QGroupBox("💡 Smart Suggestions")
            suggestions_layout = QVBoxLayout(suggestions_group)
            for suggestion in suggestions:
                label = QLabel(suggestion)
                label.setStyleSheet("color: #FCA5A5; font-size: 11px; font-weight: bold;")
                suggestions_layout.addWidget(label)
            self.dashboard_layout.addWidget(suggestions_group)
        
        # Burndown Chart
        burndown_data = self.storage.get_burndown_data(7)
        if burndown_data:
            burndown_group = QGroupBox("📉 Weekly Burndown")
            burndown_layout = QVBoxLayout(burndown_group)
            
            planned_total = max((d["planned"] for d in burndown_data.values()), default=0)
            
            # Simple ASCII-style chart
            chart_html = "<pre style='color: #00FF9C; font-size: 9px; background: #08111E; padding: 10px; border-radius: 6px;'>"
            for day_key, data in sorted(burndown_data.items())[-7:]:
                day_label = datetime.strptime(day_key, "%Y-%m-%d").strftime("%a")
                planned = data["planned"]
                completed = data["completed"]
                remaining = data["remaining"]
                
                # Bar length normalized to fit
                bar_width = int((planned / planned_total) * 20) if planned_total > 0 else 1
                complete_bar = int((completed / planned_total) * 20) if planned_total > 0 else 0
                
                bar = "█" * complete_bar + "░" * (bar_width - complete_bar)
                chart_html += f"{day_label}: {bar} {completed:.1f}h/{planned:.1f}h\n"
            chart_html += "</pre>"
            
            chart_label = QLabel(chart_html)
            chart_label.setTextFormat(Qt.TextFormat.RichText)
            burndown_layout.addWidget(chart_label)
            self.dashboard_layout.addWidget(burndown_group)
        
        # Productivity Stats
        stats = self.storage.get_productivity_stats(7)
        if stats["total_tasks"] > 0:
            stats_group = QGroupBox("📈 Weekly Stats")
            stats_layout = QVBoxLayout(stats_group)
            
            stats_html = f"""
            <p style='font-size: 11px; color: #D7E3F4; margin: 5px 0;'>
            <b>Completion Rate:</b> <span style='color: #00FF9C;'>{stats['completion_rate']:.1f}%</span><br>
            <b>Tasks Completed:</b> <span style='color: #86EFAC;'>{stats['completed_tasks']}/{stats['total_tasks']}</span><br>
            <b>Time Planned:</b> <span style='color: #7DD3FC;'>{stats['total_hours_planned']:.1f} hours</span><br>
            </p>
            """
            
            stats_label = QLabel(stats_html)
            stats_label.setTextFormat(Qt.TextFormat.RichText)
            stats_layout.addWidget(stats_label)
            self.dashboard_layout.addWidget(stats_group)
        
        self.dashboard_layout.addStretch()

    def check_reminders(self):
        if not self.storage.settings.get("reminders_enabled", True):
            return

        now = datetime.now()
        
        # Check work hours setting
        work_hours_enabled = self.storage.settings.get("work_hours_enabled", False)
        if work_hours_enabled:
            work_start = self.storage.settings.get("work_start_hour", 9)
            work_end = self.storage.settings.get("work_end_hour", 18)
            current_hour = now.hour
            
            # Skip reminders outside work hours
            if not (work_start <= current_hour < work_end):
                return

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
                        
                        # Play sound based on priority and settings
                        if self.storage.settings.get("sound_alerts_enabled", True):
                            priority = task.get("priority", "Medium")
                            sound_type = SOUND_ALERTS.get(priority, "notify")
                            play_sound(sound_type)
                        
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

    # Show main window directly
    window = MainWindow(app_icon)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec())