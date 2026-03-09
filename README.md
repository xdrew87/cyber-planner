<div align="center">

# 🍅 Cyber Planner

**An advanced, cyberpunk-themed task management and productivity application built with PyQt6**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/license-Custom-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.5-blueviolet.svg)](https://github.com/xdrew87/cyber-planner/releases/tag/v2.5)

**[Features](#-features) • [Installation](#-quick-start) • [Usage](#-usage) • [Contributing](#-contributing) • [License](#-license)**

</div>

---

## � Table of Contents

| Section | Jump To |
|---------|---------|
| **Getting Started** | [Overview](#-overview) • [Quick Start](#-quick-start) • [First 5 Minutes](#-your-first-5-minutes) |
| **Learn** | [Quick Reference](#-quick-reference-card) • [Usage Guide](#-usage-guide) • [Workflows](#-common-workflows) |
| **Features** | [Task Management](#-task-management) • [Productivity](#-productivity--analytics) • [Customization](#-customization) |
| **Troubleshoot** | [FAQ](#-frequently-asked-questions) • [Troubleshooting](#-troubleshooting) • [Help](#-author--support) |
| **Technical** | [Architecture](#-architecture) • [Dependencies](#-dependencies) • [Data Storage](#-data-storage) |
| **Project** | [License](#-license) • [Roadmap](#-roadmap---future-versions) • [Stats](#-project-statistics) |

---

Cyber Planner is a **comprehensive task management system** designed for maximum productivity. Built on a modern dark UI with cyberpunk aesthetics, it combines a full calendar interface, advanced analytics, habit tracking, and intelligent task management—all featuring keyboard shortcuts, real-time notifications, and seamless Discord integration.

**Perfect for:** 
- 💼 Project Managers (track deliverables)
- 👨‍💻 Developers (manage sprints & commits)
- 📚 Students (juggle assignments & deadlines)
- 🏃 Productivity Enthusiasts (maximize output)
- 🎯 Goal Setters (build consistent habits)

### 🎯 What Makes Cyber Planner Different?

| Traditional Apps | Cyber Planner |
|------------------|---------------|
| Cloud-dependent | 📍 100% Local Storage |
| Account required | ✅ No Login Needed |
| Limited themes | 🎨 4 Professional Themes |
| Basic tasks | 📊 Advanced analytics |
| Manual tracking | 🔥 Auto-streak habits |
| Bulky | ⚡ Lightning-fast |

### 🌟 Core Strengths

- ✅ **Zero Setup** - Open and start using immediately
- ✅ **Privacy First** - No cloud, no tracking, no accounts
- ✅ **Dark Mode Native** - Easy on the eyes
- ✅ **Keyboard Shortcuts** - Power users rejoice (press `N` for new)
- ✅ **Smart Features** - Drag-drop, recurring tasks, auto-habits
- ✅ **Extensible** - Discord webhooks, CSV export/import
- ✅ **Visual Feedback** - Real-time analytics and heatmaps

---

## ✨ Features

### 🎯 Task Management
| Feature | Description |
|---------|-------------|
| **📅 Full Calendar** | Month view with navigation and drag-drop task management |
| **✅ Create/Edit/Delete** | Intuitive dialogs for comprehensive task control |
| **🎯 Priority Levels** | Low, Medium, High with visual color-coded badges |
| **🔄 Recurring Tasks** | Daily, Weekly, Monthly auto-repeating tasks with smart generation |
| **⏰ Smart Reminders** | Customizable notifications at 15min, 5min, or at task time |
| **🔍 Search & Filter** | Quick task lookup by title, notes, category, or priority |
| **⌨️ Keyboard Shortcuts** | Press `N` for new task, `Del` to delete |

### 📊 Productivity & Analytics
| Feature | Description |
|---------|-------------|
| **🍅 Pomodoro Timer** | 25-minute focused work sessions (customizable) |
| **📈 Analytics Dashboard** | Real-time productivity tracking and statistics |
| **🔥 Daily Heatmap** | Visual activity calendar showing completion rates |
| **📉 Burndown Charts** | Track planned vs completed tasks over time |
| **💪 Habit Tracker** | Build daily habits with streak counters |
| **🤖 Smart Suggestions** | AI-powered task recommendations based on patterns |
| **📊 Weekly Review** | Automatic weekly statistics and progress reports |

### 🎨 Customization
| Feature | Description |
|---------|-------------|
| **🎨 4 Built-in Themes** | Cyberpunk, Purple Dream, Ocean Blue, Neon Pink |
| **🖼️ Custom Backgrounds** | Support for PNG, JPG, and animated GIFs |
| **⚙️ 7 Settings Tabs** | Notifications, Themes, Time, Productivity, Display, Backgrounds, Data |
| **🔔 Notification Control** | Customize sounds, tray alerts, Discord webhooks |
| **📺 Display Settings** | Font sizes, always-on-top mode, notification positions |

### 🔌 Integration & Export
| Feature | Description |
|---------|-------------|
| **🔔 Discord Webhooks** | Real-time task reminders to Discord channels |
| **💾 CSV Export/Import** | Backup tasks or migrate from other apps |
| **🖥️ System Tray** | Minimize to tray with system notifications |
| **🔐 Local Storage** | JSON-based persistence (no cloud required) |

---

## 🆕 What's New in v2.5

**Major Release - Complete Productivity Suite**

```
✨ 4 Professional Color Themes        💪 Daily Habit Tracking with Streaks
📊 Advanced Analytics Dashboard        🎯 Tabbed Settings Organization  
🤖 Smart Task Suggestions              🖼️ Improved GIF Background Support
```

### Changes from v2.0
- ✅ Removed login/profile system (single-user for GitHub)
- ✅ Added theme system (4 color palettes)
- ✅ Complete habit tracking module
- ✅ Advanced analytics with charts and heatmaps
- ✅ Reorganized settings into 7 specialized tabs
- ✅ Improved background management
- ✅ Performance optimizations & bug fixes

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **pip** (usually included with Python)
- **6 MB** disk space for application

### Installation (3 minutes)

#### Method 1: From Repository (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/xdrew87/cyber-planner.git
cd cyber-planner

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

#### Method 2: Build as Standalone EXE (Windows)

```bash
# Clone and navigate to directory
git clone https://github.com/xdrew87/cyber-planner.git
cd cyber-planner

# Install dependencies
pip install -r requirements.txt

# Build executable
./build_exe.bat

# Run from dist/ folder
./dist/Cyber\ Planner.exe
```

### First Launch

✅ **On first launch:**
- Application creates `tasks.json` and `settings.json` automatically
- Default theme is set to "Cyberpunk" 
- Background folder is created in `backgrounds/`
- Ready to add your first task! Press `N` or click **+ Add Task**

### 🎬 Your First 5 Minutes

```
0:00 → Launch app (no setup!)
0:30 → Press 'N' to create your first task
2:00 → See it appear in calendar
3:00 → Click Settings to customize theme
4:00 → Try Pomodoro timer
5:00 → You're productive! 🚀
```

---

## 🗺️ App Layout Overview

```
┌─────────────────────────────────────────────────┐
│  📅 Cyber Planner                   ⚙️ Settings │
├──────────────┬──────────────────────┬───────────┤
│              │                      │           │
│   Calendar   │  Task Details        │ Analytics │
│   (left)     │  (center)            │  (right)  │
│              │  [Task List]         │  📊 Stats │
│ ◀ Preview   │  [Edit/Delete]       │  🔥 Habits│
│ ▶ Next      │  [Search/Sort]       │  📈 Charts│
│              │                      │           │
├──────────────┴──────────────────────┴───────────┤
│ ⏱️ Pomodoro    🍅 Timer    ⚡ Quick Actions   │
└─────────────────────────────────────────────────┘
```

---

## 💻 System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 7+, macOS, Linux |
| **Python** | 3.8+ |
| **Memory** | ~100 MB |
| **Disk** | 50 MB (including dependencies) |
| **GUI** | PyQt6 + system windowing |

---

## ⌨️ Quick Reference Card

### 🚀 Keyboard Shortcuts

| Shortcut | Action | Context |
|----------|--------|---------|
| `N` | Create new task | Global |
| `Del` | Delete selected task | Task list |
| `Ctrl+S` | Save/Export tasks | (Auto-saved) |
| `Esc` | Close dialogs | Any dialog |
| `Right Arrow` | Next month | Calendar |
| `Left Arrow` | Previous month | Calendar |

### 💡 UI Quick Access

| Element | Purpose | Location |
|---------|---------|----------|
| **+ Add Task** | New task | Top header |
| **Settings** | Preferences | Top header |
| **≡ Menu** | Import/Export | Top header |
| **Calendar** | View/edit by date | Left panel |
| **Analytics** | Productivity stats | Right panel |
| **Habits** | Track daily habits | Sidebar |
| **Pomodoro** | Focus timer | Toolbar |

---

## 📖 Usage Guide

### 🎯 Creating Tasks

**Via Button:**
1. Click **+ Add Task** button in header
2. Fill in task details:
   - **Title** (required) - Task name
   - **Time** - Task start time (24-hour format)
   - **Duration** - How long it will take (Minutes/Hours/Days)
   - **Category** - Organization (Work, Personal, Urgent, Coding, etc.)
   - **Priority** - Importance level (Low/Medium/High)
   - **Energy Level** - Required mental energy (Low/Medium/High)
   - **Recurring** - Auto-repeat (None/Daily/Weekly/Monthly)
   - **Status** - Current state (Not Started/In Progress/Completed)
   - **Notes** - Additional details
3. Click **OK**

**Via Keyboard:**
- Press `N` anywhere to open new task dialog

### ✅ Managing Tasks

| Action | Method |
|--------|--------|
| **Edit Task** | Right-click task → Edit |
| **Duplicate** | Right-click task → Duplicate |
| **Delete** | Right-click task → Delete or press `Del` |
| **Mark Complete** | Check the checkbox next to task |
| **Drag to Date** | Drag task from one calendar day to another |

### 🔍 Finding Tasks

**Search Bar:**
```
Type to filter tasks by:
- Task title
- Notes content
```

**Sort Dropdown:**
```
Organize by:
- Time (earliest first)
- Duration (longest first)
- Category (alphabetical)
```

**Manual Filtering:**
- Click calendar dates to view specific day
- Use navigation arrows (◀ Prev / Next ▶) for months

### 🎨 Changing Themes

1. Click **Settings** button
2. Go to **🎨 Themes** tab
3. Select from dropdown:
   - **Cyberpunk** - Neon green (#00FF9C) - Default
   - **Purple Dream** - Violet accents
   - **Ocean Blue** - Cyan highlights
   - **Neon Pink** - Hot pink accents
4. Preview updates in real-time
5. Click **Save**

### 🖼️ Setting Backgrounds

1. Click **Settings** button
2. Go to **🖼️ Backgrounds** tab
3. **Choose from presets:**
   - ➖ None (dark background)
   - 🎬 Bundled GIFs and images
4. **Or load custom:**
   - Click **📂 Load Custom Background**
   - Select PNG, JPG, or GIF file
   - Preview appears instantly
5. Click **Save**

### 💪 Tracking Habits

1. Click **+ Add Habit** (sidebar)
2. Set habit parameters:
   - Habit name (e.g., "Morning workout")
   - Frequency (Daily/Weekdays/Weekends/Weekly)
   - Category (Health/Learning/Personal/Work/Fitness)
   - Reminder time
   - Notes (why it's important)
3. Check off daily to build streaks
4. View streak progress in sidebar

### 📊 Viewing Analytics

**Access via:**
- Dashboard tab (right panel)
- Automatically calculated for last 7 days

**Available Metrics:**
- **Productivity Stats** - Tasks completed, completion rate
- **Daily Heatmap** - Visual activity calendar
- **Burndown Chart** - Planned vs completed over time
- **Smart Suggestions** - Task recommendations

### 🍅 Using Pomodoro Timer

1. Select a task
2. Click **🍅 Pomodoro** button
3. Timer dialog opens (25 min default)
4. Click **Start** to begin
5. App displays countdown
6. Get notified when 25 minutes complete
7. Can customize duration in **Settings → 🎯 Productivity**

### ⏰ Setting Reminders

Task reminders notify you:
- **15 minutes** before task time
- **5 minutes** before task time  
- **At task time**

**Configure via:**
- Settings → 🔔 Notifications → "Reminders"
- Enable/disable as needed

### 🔔 Discord Notifications

1. Create Discord webhook URL:
   - Go to Discord server → Settings → Webhooks
   - Create New Webhook
   - Copy webhook URL
2. In app: Settings → 🔔 Notifications
3. Paste webhook URL
4. Click **Save**
5. Task reminders now post to Discord!

### 💾 Backup & Export

**Manual Export:**
1. Click **≡ Menu**
2. Select **Export to CSV**
3. Choose save location
4. Tasks saved as `tasks.csv`

**Manual Import:**
1. Click **≡ Menu**
2. Select **Import from CSV**
3. Select CSV file
4. Tasks merged into planner

**Auto-Backup:**
1. Settings → 💾 Data
2. Enable "Auto-backup"
3. Choose frequency (daily/weekly/monthly)
4. Backups stored in `~/.cyber-planner/backups/`

---

---

## 📊 Feature Comparison vs Similar Apps

| Feature | Cyber Planner | Todoist | Notion | Apple Reminders |
|---------|---------------|---------|--------|-----------------|
| **Local Storage** | ✅ 100% | ❌ Cloud only | ⚠️ Hybrid | ✅ iCloud sync |
| **Dark Theme** | ✅ 4 themes | ⚠️ Basic | ✅ Yes | ✅ Yes |
| **Habit Tracking** | ✅ Built-in | ⚠️ Add-on | ✅ Yes | ❌ No |
| **Analytics** | ✅ Advanced | ⚠️ Limited | ✅ Advanced | ❌ No |
| **Discord Integration** | ✅ Webhooks | ❌ No | ❌ No | ❌ No |
| **Pomodoro Timer** | ✅ Built-in | ❌ No | ❌ No | ❌ No |
| **No Login Required** | ✅ Yes | ❌ Account required | ❌ Account required | ❌ Apple ID |
| **Price** | 🆓 Free | 💰 $4/mo | 💰 $5-10/mo | 🆓 Free |
| **Data Export** | ✅ CSV | ⚠️ Limited | ✅ Full | ⚠️ Limited |
| **Customization** | ✅ Full | ⚠️ Limited | ✅ Full | ⚠️ Basic |

---

## 📁 Project Structure & File Guide

```
cyber-planner/
│
├── 📄 main.py                    # Main application (3,600+ lines)
│                                  # Classes: MainWindow, Storage, Dialogs
│                                  # Features: All UI, logic, helpers
│
├── 📋 requirements.txt           # Python dependencies
│                                  # PyQt6>=6.0.0
│                                  # requests>=2.25.0
│
├── 🔧 build_exe.bat             # Windows EXE builder script
│                                  # Runs: pyinstaller + icon bundling
│                                  # Creates: dist/Cyber\ Planner.exe
│
├── 📝 README.md                  # This file (documentation)
├── 📜 LICENSE                    # Custom License terms
├── 📋 setup.py                   # Python package installer
│
├── 💾 Data Files (Auto-created)
│   ├── tasks.json               # All tasks by date
│   └── settings.json            # User preferences
│
├── 🖼️ backgrounds/              # Custom backgrounds folder
│   └── (user adds PNG/JPG/GIF)
│
├── 🎨 cyber_planner2.ico        # Application icon (4KB)
│
└── 📦 __pycache__/              # Python cache (ignore)
```

### 📊 Key Files Detail

**`main.py` - The Core Application**
- 3,600+ lines of Python
- PyQt6 GUI framework
- Complete task management
- All analytics, habits, timers
- Single-file distribution (no dependencies except PyQt6 + requests)

**`tasks.json` - Your Task Data**
```json
{
  "2024-03-09": [
    {
      "id": "uuid-12345",
      "title": "Fix bug #123",
      "time": "14:30",
      "duration_minutes": 120,
      "category": "Coding",
      "priority": "High",
      "recurring": "None",
      "completed": false,
      "notes": "Critical performance issue"
    }
  ]
}
```

**`settings.json` - Your Preferences**
```json
{
  "theme_name": "Cyberpunk",
  "reminders_enabled": true,
  "pomodoro_duration": 25,
  "discord_webhook_url": "https://...",
  "custom_categories": ["Work", "Personal", "Urgent", "Coding"],
  "background_file": "200.gif"
}
```

### 🔒 Privacy & Security
- ✅ All data stored **locally** (no cloud sync)
- ✅ No telemetry or tracking
- ✅ No authentication required
- ✅ Credentials stored in `settings.json` (not uploaded)

---

## 🏗️ Architecture

### Main Classes

| Class | Purpose | Lines |
|-------|---------|-------|
| **Storage** | JSON persistence layer | ~200 |
| **MainWindow** | Main application UI | ~1500 |
| **AddTaskDialog** | Task creation/editing | ~200 |
| **SettingsDialog** | Settings UI with tabs | ~500 |
| **HabitDialog** | Habit creation/editing | ~100 |
| **PomodoroDialog** | Pomodoro timer UI | ~100 |
| **DraggableTaskList** | Drag-drop task list | ~80 |
| **DayCell** | Calendar day cell | ~150 |

### Technology Stack

| Technology | Purpose | Version |
|-----------|---------|---------|
| **PyQt6** | GUI Framework | 6.0+ |
| **Python** | Runtime | 3.8+ |
| **JSON** | Data Storage | Native |
| **requests** | Discord Integration | 2.25+ |
| **winsound** | Notifications | Native (Windows) |

### Code Metrics
- **Total Lines:** 3,600+
- **Functions:** 100+
- **Classes:** 8
- **Features:** 50+

---

## ✨ Pro Tips & Power User Features

### ⚡ Speed Tricks

| Trick | What it does | Time Saved |
|-------|-------------|-----------|
| Press `N` anywhere | Instant new task | 0.5 sec |
| Drag task to date | Move don't re-add | 2 sec |
| Right-click task | Quick actions menu | 1 sec |
| `Ctrl+S` | Force save | Ensures backup |
| Click date number | Jump to day view | 1 click |

### 🎯 Productivity Hacks

**The "5-Minute Rule"**
- Schedule ANY task that takes 5 min or less
- Do it immediately
- Boosts sense of progress
- Example: "Reply to 3 emails" = 5 min task

**The "Three Big Rocks"**
1. Every morning, pick 3 main tasks
2. Do them before checking other stuff
3. Rest of day = bonus wins

**The "Pomodoro+Habit" Combo**
1. Set habit to "Before Pomodoro"
2. Each Pomodoro = 1 habit point
3. Run 4-6 Pomodoros daily
4. Automatic 4-6 habit streaks

**The "Analytics Audit"**
- Every Friday: Open Analytics tab
- Look at heatmap (green = productive)
- Copy patterns from top days
- Next week: repeat what works

### 🔥 Advanced Features

**Recurring Tasks Smart Behavior:**
- Daily: Repeats every day at same time
- Weekly: Repeats same day next week
- Monthly: Repeats same date next month
- Automatically creates next instance

**Multi-Task Drag Selection:**
- While dragging, hold `Shift`
- Select multiple tasks
- Drag all together

**Category Color Coding:**
- Each category gets auto-color
- Customize in Settings → Display
- Eye-scan your priorities instantly

**Discord Webhook Timing:**
- Sends 15 min before reminder
- Posts to specific channel
- Includes task details + priority
- Works offline (queued locally)

**CSV Import Smart Merge:**
- Importing doesn't delete existing
- Duplicates are ignored by ID
- Perfect for bulk updates
- Backup first if unsure!

---

## 🐛 Troubleshooting

### 🔴 Critical Issues

#### Application Won't Start

**Error: "ModuleNotFoundError: No module named 'PyQt6'"**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Error: "Icon file not found"**
```bash
# Solution: Ensure cyber_planner2.ico is in same directory
# The app will work without it but tray icon won't display
# Workaround: Download icon file or create a 16x16 placeholder
```

**Error: "Port already in use" (Discord)**
- Another instance is running
- Close existing Cyber Planner window
- Restart application

### 🟡 Data Issues

#### Tasks Not Saving
| Issue | Check | Solution |
|-------|-------|----------|
| Tasks disappear on close | Disk space | `wmic logicaldisk get size,freespace` |
| JSON corruption | File integrity | Restore from backup in `.cyber-planner/backups/` |
| Permission denied | Write access | `icacls tasks.json /grant "*":F` |
| File locked | Another process | Close all instances and restart |

#### Tasks Disappeared Completely
```bash
# Restore most recent backup
cd ~/.cyber-planner/backups/
ls -la backup_*.json
cp backup_LATEST.json ../../../tasks.json
# Restart app
```

### 🟡 Notification Issues

#### Reminders Not Working

**Checklist:**
- [ ] Desktop notifications enabled (Windows Settings → Notifications)
- [ ] Reminders enabled (Settings → Notifications → "Reminders")
- [ ] System volume is ON
- [ ] Task has a time set
- [ ] Current time is not past reminder time

**Discord-specific Issues:**

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid webhook URL | Create new webhook in Discord |
| 404 Not Found | Channel/webhook deleted | Recreate webhook, update URL |
| 429 Too Many Requests | Rate limited | Don't create 100+ tasks instantly |
| No message posted | Wrong channel | Double-check webhook channel |

### 🟡 Display Issues

#### Reminders Not Working

**Problem:** Tasks disappear after closing app

**Causes & Solutions:**
1. Check disk space
   ```bash
   # Windows
   wmic logicaldisk get size,freespace
   ```
2. Verify write permissions
   ```bash
   # Check tasks.json is writable
   chmod u+w tasks.json
   ```
3. Check file corruption
   ```bash
   # Restore from backup
   cp ~/.cyber-planner/backups/backup_*.json tasks.json
   ```

#### Background/GIF Not Displaying

**"GIF not animating"**
- Ensure file is valid GIF format
- Try a different GIF
- Recommended size: <5 MB
- Test with bundled GIF first

**"Image appears stretched/squashed"**
- App scales to window size
- Use wider aspect ratio images (16:9 recommended)
- Try 1920x1080 for full HD monitors

**"Background disappeared after theme change"**
- Backgrounds don't persist on theme switch in v2.5
- Re-select background after switching themes
- This is fixed in v2.6+

### 🟡 Performance Issues

#### App is Slow/Laggy

**Quick fixes (in order):**
1. Close other applications
2. Check system RAM: `wmic OS get TotalVisibleMemorySize`
3. Disable animations: Settings → Display → "Animations"
4. Reduce number of tasks on screen (archive old tasks)
5. Restart application fresh

**Memory usage high?**
- Close unused dialogs
- Don't keep Settings or Pomodoro open
- Restart the app
- Check if Window is actually minimized/hidden

#### Many Tasks = Slow Calendar

**Solution:**
- Archive completed tasks to CSV
- Keep active tasks only (< 200)
- Organize: 2024, 2025 folders later

---

## � Common Workflows

### 📅 "Plan My Week" Workflow

```
1. Open app (Sunday evening)
2. View calendar → Next week
3. Press 'N' → Add 5-7 main tasks
4. Set duration for each
5. Enable recurring if needed
6. Set reminders (15 min before each)
7. Check analytics → Set realistic expectations
8. Save → Done!
```

### 🎯 "Complete a Task" Workflow

```
1. Find task in calendar or search
2. Click to view details
3. Start Pomodoro timer (if long task)
4. Work on task
5. Check 'Complete' when done
6. Habit streak updates automatically
7. Analytics refreshed in real-time
```

### 🔥 "Build a Habit" Workflow

```
1. Click "Add Habit"
2. Name: "Morning Yoga" 
3. Frequency: Weekdays (Mon-Fri)
4. Reminder: 7:00 AM
5. Click "Create"
6. Check off each day
7. Streak shown in sidebar
8. Challenge: 30-day streak
```

### 🎨 "Customize the Look" Workflow

```
1. Settings → Themes tab
2. Switch theme:
   - Cyberpunk (default green)
   - Purple Dream (royal violet)
   - Ocean Blue (cyan)
   - Neon Pink (hot pink)
3. Real-time preview
4. Settings → Backgrounds tab
5. Select GIF or image
6. Save → Instant refresh
```

### 📊 "Weekly Review" Workflow

```
1. Every Friday evening:
2. Open app → Analytics tab
3. Check:
   - Tasks completed (%)
   - Productivity heatmap
   - Habit streaks
   - Burndown chart
4. Plan next week based on metrics
5. Export to CSV for records
6. Celebrate wins! 🎉
```

### 🔔 "Discord Reminders" Workflow

```
1. Create Discord server webhook:
   - Server Settings → Webhooks
   - "New Webhook"
   - Copy URL
2. In app: Settings → Notifications
3. Paste webhook URL
4. Enable Discord reminders
5. Save
6. Next reminder → Posts to Discord automatically
```

---

## ❓ Frequently Asked Questions

### 🚀 Getting Started

**Q: How do I add my first task?**
A: Press `N` or click "+ Add Task" in the header. Fill in the title and click OK. You're done!

**Q: What's the difference between duration and time?**
A: **Time** is when the task starts (14:30). **Duration** is how long it takes (2 hours). Both optional.

**Q: Can I move tasks to different dates?**
A: Yes! Drag tasks in the calendar. Or edit the task and change the date field.

**Q: Do I need an account?**
A: No! This is a local app. No login, no cloud, no accounts needed.

### 💾 Data & Backup

**Q: Where are my tasks stored?**
A: In `tasks.json` in the app folder (not uploaded anywhere).

**Q: Can I backup my tasks?**
A: Yes, 3 ways:
1. Enable auto-backup in Settings
2. Export to CSV manually (≡ Menu → Export)
3. Copy `tasks.json` to safe location

**Q: How do I restore from backup?**
A: Replace `tasks.json` with your backup copy and restart the app.

**Q: Can I sync across devices?**
A: Not built-in, but you can:
1. Export CSV from one device
2. Import CSV on another device

### ⏰ Reminders & Notifications

**Q: Why aren't reminders working?**
A: Check:
- Desktop notifications enabled (Windows Settings)
- Reminders enabled in app (Settings → Notifications)
- System volume is on
- Task time is set correctly

**Q: Can I customize reminder times?**
A: Partially. You can:
- Choose: at time, 5 min before, or 15 min before
- Customize Pomodoro duration
- Set custom category colors

**Q: Do I need Discord for reminders?**
A: No! Desktop notifications work without Discord. Discord is optional.

### 🎨 Themes & Customization

**Q: How do I change themes?**
A: Settings → Themes → Select from dropdown → Save

**Q: Can I create custom themes?**
A: Not via UI currently, but you can:
1. Edit `settings.json`
2. Modify color hex values
3. Restart app (advanced users)

**Q: Can I use animated GIFs as backgrounds?**
A: Yes! Supports PNG, JPG, and GIF. Animated GIFs play automatically.

**Q: Why is my background stretched/squashed?**
A: Background scales to window size. Use wider aspect ratio images (16:9 recommended).

### 🍅 Pomodoro & Productivity

**Q: How long is a Pomodoro session?**
A: Default 25 minutes, but you can change it.

**Q: Can I pause/resume the timer?**
A: The timer runs - you can start/stop the dialog, but the countdown continues.

**Q: Does Pomodoro sync with tasks?**
A: No, it's separate. But starting Pomodoro from a task marks progress.

**Q: What's the ideal Pomodoro duration for me?**
A: Most people use 25 min. Try 20-45 min to find your sweet spot.

### 💪 Habits & Streaks

**Q: How do I track a habit?**
A: Add Habit → Name it → Set frequency → Check off each day

**Q: Can habits repeat multiple times per day?**
A: Currently: once per day only. Workaround: Create multiple habits.

**Q: What happens if I miss a day?**
A: Streak resets to 0. No penalty, just a new challenge!

**Q: Can I see historical habit data?**
A: Streak number shown. Full history in `settings.json`.

### 📊 Analytics & Reports

**Q: What do the analytics numbers mean?**
A:
- **Completion %**: Tasks marked done / total tasks
- **Heatmap**: Green = most productive days
- **Burndown**: Planned vs actual completion
- **Streaks**: Current habit chains

**Q: How far back do analytics go?**
A: Currently last 7 days. Full history saved for future versions.

**Q: Can I export analytics?**
A: Export tasks as CSV (includes completion status). Use Excel for pivot tables.

### ⚙️ Performance & Troubleshooting

**Q: App is slow/laggy. What do I do?**
A: Try:
1. Close other apps
2. Reduce animation effects (Settings → Display)
3. Restart the app
4. Check disk space

**Q: Tasks keep disappearing!**
A: Check:
- Disk space available
- File permissions on `tasks.json`
- Not editing JSON manually
- Enable auto-backup to prevent loss

**Q: Can I export and import tasks?**
A: Yes! ≡ Menu → Export to CSV → Share anywhere
Then ≡ Menu → Import from CSV → Merge into app

### 🔧 Advanced & Technical

**Q: Can I modify the code?**
A: Sure! It's open for personal use. You can:
- Fork for yourself locally
- Modify colors, behavior, etc.
- Can't redistribute (Custom License)

**Q: How do I build the EXE myself?**
A: Run `./build_exe.bat` (Windows). Requires PyInstaller.

**Q: What Python version do I need?**
A: 3.8 or newer. Check: `python --version`

**Q: Can I run this on macOS/Linux?**
A: Yes! Same code, but:
- Activate venv differently
- Webhook URLs same
- Icons might differ

---

## �📦 Dependencies

### Required
```
PyQt6>=6.0.0              # GUI Framework
requests>=2.25.0          # HTTP requests (Discord)  
```

### Optional (for building EXE)
```
PyInstaller>=4.5          # Executable builder
```

### Windows-specific
```
winsound                  # System sounds (built-in)
```

Full dependency list: [`requirements.txt`](requirements.txt)

---

## 🔐 Security Notes

### Data Privacy
- **No cloud storage** - All data stays on your computer
- **No accounts** - No login, no tracking
- **No telemetry** - App doesn't phone home
- **No permissions** - Only accesses files you explicitly open

### Discord Integration
- Webhook URLs can be exposed in process list
- **Recommendation:** Use environment variables
  ```bash
  set DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/...
  python main.py
  ```

### File Permissions
- `tasks.json` - Should be readable/writable by user only
- Backups stored in `~/.cyber-planner/backups/` - Hidden directory on most systems

---

## 🤝 Contributing

While this project uses a **Custom License** (not open source), you can:

1. **Report Issues** - Open GitHub issues if you find bugs
2. **Suggest Features** - Share ideas in Discussions (no guarantee they'll be implemented)
3. **Fork for Personal Use** - Create your own fork for personal customization
4. **Local Development** - Modify the code for your own use locally

⚠️ **Note:** Pull requests and redistribution are **not permitted** under the Custom License. This project is for personal and custom implementation use only.

---

## 📝 License

**© 2026 - All rights reserved**

This project is provided under a **Custom License**. See [LICENSE](LICENSE) file for details.

### Usage Rights
✅ **Allowed:**
- Personal use
- Custom implementations
- Educational purposes
- Local deployments

❌ **Not Allowed Without Permission:**
- Commercial redistribution
- Hosting as a service
- Rebranding
- Closed-source modifications

For commercial licensing, contact the author.



---

## 🎨 Design & Aesthetics

### Color Palettes

**Cyberpunk** (Default)
- Primary: `#00FF9C` (Neon Green)
- Background: `#05080F` (Deep Blue-Black)
- Accent: `#7DD3FC` (Light Blue)

**Purple Dream**
- Primary: `#B366FF` (Violet)
- Background: `#0F0B1E` (Dark Purple)
- Accent: `#9945FF` (Purple)

**Ocean Blue**
- Primary: `#00D9FF` (Cyan)
- Background: `#0A1628` (Navy)
- Accent: `#0099FF` (Blue)

**Neon Pink**
- Primary:` #FF0080` (Hot Pink)
- Background: `#1A0F15` (Dark Maroon)
- Accent: `#FF1493` (Deep Pink)

### Typography
- **Font:** Segoe UI / Consolas
- **Body:** 11px
- **Headers:** 14px bold
- **Monospace:** 10px (for times/codes)

---

## 🔮 Roadmap

### Planned Features (Future Versions)
- [ ] Cloud synchronization (optional)
- [ ] Mobile app / web version
- [ ] Task templates library
- [ ] Team collaboration
- [ ] Advanced filtering/saved views
- [ ] Calendar integrations (Google, Outlook)
- [ ] Time tracking with auto-pause
- [ ] AI-powered scheduling
- [ ] Custom notifications sounds
- [ ] Voice commands

### Under Consideration
- Performance metrics
- Budget/expense tracking
- Team sharing
- API for integrations
- Plugin system

---

## 📊 Statistics

- **First Release:** 2024
- **Current Version:** 2.5
- **Code Size:** 3,600+ lines
- **Supported Platforms:** Windows, macOS, Linux
- **Python Support:** 3.8+
- **License:** Custom

---

<div align="center">

---

## 🎓 Learning Resources

### 📚 How-To Guides
- **New User?** Start with [Quick Start](#-quick-start) section
- **Need Help?** Check [FAQ](#-frequently-asked-questions) section
- **Found a Bug?** See [Troubleshooting](#-troubleshooting) section
- **Want More?** Read [Usage Guide](#-usage-guide) in detail

### 🎬 Getting Started Path
1. First Task (2 min) - Press N, fill form, save
2. Themes (1 min) - Settings → Themes → Choose
3. Habits (2 min) - Add Habit → Check daily
4. Analytics (3 min) - Open Analytics tab, explore charts
5. Pomodoro (1 min) - Start timer, focus intensely

### 💬 Getting Help
1. **Search this README** (Ctrl+F) - Most questions answered here
2. **Check FAQ** - Common issues and solutions
3. **Troubleshooting** - Specific problem-solving guides
4. **GitHub Issues** - Report bugs with reproduction steps

---

## 🚀 Quick Links

| Need | Action |
|------|--------|
| **Install** | Go to [Quick Start](#-quick-start) |
| **First Use** | Read [Your First 5 Minutes](#-your-first-5-minutes) |
| **Keyboard Tricks** | See [Quick Reference](#-quick-reference-card) |
| **Learning** | Try [Common Workflows](#-common-workflows) |
| **Problems?** | Search [Troubleshooting](#-troubleshooting) |
| **Questions?** | Check [FAQ](#-frequently-asked-questions) |
| **Details** | See [Full Usage Guide](#-usage-guide) |
| **Code** | View [Architecture](#-architecture) |
| **License** | Read [License](#-license) |

---

## 👨‍💻 Author & Support

**Developer:** [galmx (xdrew87)](https://github.com/xdrew87)  
**GitHub:** [@xdrew87](https://github.com/xdrew87)  
**Repository:** [cyber-planner](https://github.com/xdrew87/cyber-planner)  
**Issues:** [GitHub Issues Board](https://github.com/xdrew87/cyber-planner/issues)  
**Discussions:** [GitHub Discussions](https://github.com/xdrew87/cyber-planner/discussions)

### Getting Help - Best Practices

**🟢 Before Opening an Issue:**
- [ ] Search existing issues (someone might have solved it)
- [ ] Check Troubleshooting section (common fixes)
- [ ] Review FAQ (quick answers)
- [ ] Verify Python version: `python --version`
- [ ] Verify dependencies: `pip list | grep PyQt6`

**🟡 When Opening an Issue, Include:**
- Python version (`python --version`)
- Operating system (Windows 10, macOS Big Sur, etc.)
- Exact error message (copy-paste)
- Steps to reproduce
- What you were trying to do
- Screenshot if possible

**🔴 Emergency - App Crashed:**
1. Restore from backup (`~/.cyber-planner/backups/`)
2. File issue with error message
3. We'll help you recover

---

## 🎨 Design & Aesthetics

### 🌈 Color Palettes

**Cyberpunk** (Default - 🎯 RECOMMENDED)
```
Primary:     #00FF9C (Neon Green)
Background:  #05080F (Deep Blue-Black)
Accent:      #7DD3FC (Light Blue)
Text:        #FFFFFF (Pure White)
Feeling:     High-energy, tech, futuristic
```

**Purple Dream**
```
Primary:     #B366FF (Violet)
Background:  #0F0B1E (Dark Purple)
Accent:      #9945FF (Purple)
Text:        #E8D9FF (Light Lavender)
Feeling:     Creative, calm, artistic
```

**Ocean Blue**
```
Primary:     #00D9FF (Cyan)
Background:  #0A1628 (Navy)
Accent:      #0099FF (Blue)
Text:        #E0F7FF (Light Cyan)
Feeling:     Cool, professional, water-like
```

**Neon Pink**
```
Primary:     #FF0080 (Hot Pink)
Background:  #1A0F15 (Dark Maroon)
Accent:      #FF1493 (Deep Pink)
Text:        #FFE4FA (Light Pink)
Feeling:     Bold, energetic, vibrant
```

### 📐 Typography

| Element | Font | Size | Weight | Usage |
|---------|------|------|--------|-------|
| **Headers** | Segoe UI | 14px | Bold | Section titles |
| **Body Text** | Segoe UI | 11px | Regular | Form labels, dialogs |
| **Monospace** | Consolas | 10px | Regular | Times, codes, paths |
| **Buttons** | Segoe UI | 11px | Semi-bold | Action buttons |

---

## 🔮 Roadmap - Future Versions

### v2.6 (Next Release)
- [ ] Persistent backgrounds on theme switch
- [ ] Custom theme creator
- [ ] Improved mobile responsiveness
- [ ] Dark/light mode toggle

### v3.0 (Major Release)
- [ ] Cloud sync option (optional)
- [ ] Mobile app (iOS/Android)
- [ ] Team collaboration
- [ ] API for integrations
- [ ] Advanced filtering with saved views

### Under Research
- Voice commands
- AI-powered scheduling
- Budget/expense tracking
- Plugin system
- Custom notification sounds

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Version** | 2.5 |
| **Release Date** | 2024 |
| **Code Size** | 3,600+ lines |
| **Classes** | 8 main classes |
| **Functions** | 100+ functions |
| **Features** | 50+ features |
| **Supported Platforms** | Windows, macOS, Linux |
| **Python Version** | 3.8+ |
| **License** | Custom (All rights reserved) |
| **Last Updated** | 2026 |

---

## 🤝 Support This Project

### Ways to Support
- ⭐ Star this repository
- 🐛 Report bugs and suggest features
- 📝 Improve documentation
- 📤 Share with friends
- 💬 Give feedback

### Star History
If you find Cyber Planner useful:
1. Click the **⭐ Star** button at top of repo
2. Helps others discover the project
3. Shows project is valuable
4. Costs you nothing!

---

<div align="center">

### 🌟 Made with ❤️ for productivity enthusiasts

**Questions?** Check the [FAQ](#-frequently-asked-questions) | **Issues?** See [Troubleshooting](#-troubleshooting) | **Want to help?** Read [Contributing](#-contributing)

---

**[Back to Top](#-cyber-planner)** • **[Quick Start](#-quick-start)** • **[GitHub](https://github.com/xdrew87/cyber-planner)** • **[Issues](https://github.com/xdrew87/cyber-planner/issues)**

---

© 2024-2026 Cyber Planner • All rights reserved • Custom License

</div>
