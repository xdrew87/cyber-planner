# 🍅 Cyber Planner v2.0

A powerful, dark-themed task scheduling and planning application built with PyQt6. Features include a full calendar, task management, Pomodoro timer, recurring tasks, priority levels, and more.

**Made by:** [galmx (xdrew87)](https://github.com/xdrew87)

## ✨ Features

- **📅 Full Calendar** - Month navigation with drag-drop task management
- **✅ Task Management** - Create, edit, duplicate, and delete tasks
- **🎯 Priority Levels** - Low, Medium, High priority with visual badges
- **🔄 Recurring Tasks** - Daily, Weekly, Monthly auto-repeating tasks
- **🍅 Pomodoro Timer** - Built-in 25-minute productivity sessions
- **⏰ Smart Reminders** - Notifications at 15min, 5min, and at task time
- **🔔 Discord Integration** - Webhook notifications for task reminders
- **📊 Weekly Analytics** - Track task counts and time breakdown by category
- **🎨 Custom Backgrounds** - Support for images and GIF animations
- **💾 CSV Import/Export** - Backup and migrate your tasks
- **🖥️ System Tray** - Minimize to tray with notifications
- **⌨️ Keyboard Shortcuts** - Quick commands (N for new, Del to delete)
- **🌙 Dark Cyberpunk Theme** - Eye-friendly dark UI with neon accents

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PyQt6
- requests

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/xdrew87/cyber-planner.git
   cd cyber-planner
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## 📦 Building as Executable

Convert to a standalone Windows .exe using PyInstaller:

```bash
./build_exe.bat
```

Your executable will be in `dist/Cyber Planner.exe`

### Build Requirements
- PyInstaller (installed automatically by build script)
- Bundled GIFs: `smoke.gif`, `jin.gif`, `simpsons-desk.gif`  

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `N` | Create new task |
| `Del` | Delete selected task |

## 🎯 Usage

### Creating a Task
1. Click **+ Add Task** or press `N`
2. Enter task details:
   - Title (required)
   - Time
   - Duration
   - Category
   - Priority (Low/Medium/High)
   - Recurring (None/Daily/Weekly/Monthly)
   - Notes
3. Click **OK**

### Managing Tasks
- **Edit**: Right-click → Edit
- **Duplicate**: Right-click → Duplicate
- **Delete**: Right-click → Delete or press `Del`
- **Mark Complete**: Check the checkbox

### Searching & Sorting
- Use **Search** bar to filter by title or notes
- Use **Sort by** dropdown to organize by Time, Duration, or Category
- **Priority sorting** always shows High→Medium→Low first

### Quick Actions
- **⏰ Snooze**: Move selected task to tomorrow
- **🍅 Pomodoro**: Start 25-minute timer for selected task

### Settings
- Discord webhook notifications
- Enable/disable reminders
- Enable/disable tray notifications

### Background Customization
Click **Background** button to:
- Select custom image or GIF (PNG, JPG, GIF supported)
- Switch between bundled backgrounds (200.gif, jin.gif, simpsons-desk.gif)

## 📊 Data & Persistence

Your data is stored locally as JSON:
- **tasks.json** - All tasks and schedules
- **settings.json** - User preferences and configuration

Data persists between sessions automatically.

## 🔐 Discord Webhook Integration

Set your Discord webhook for notifications:

### Method 1: Environment Variable (Recommended)
```bash
set DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/...
python main.py
```

### Method 2: Settings UI
1. Click **Settings**
2. Enter Discord webhook URL
3. Save

**Note:** Environment variable overrides saved setting.

## 📋 Categories

Default categories:
- Work
- Personal
- Urgent
- Coding

Customize via `settings.json` under `custom_categories`.

## 🛠️ Architecture

```
main.py
├── Storage          # JSON persistence layer
├── AddTaskDialog    # Task creation/editing dialog
├── SettingsDialog   # Settings dialog
├── PomodoroDialog   # Pomodoro timer dialog
├── DraggableTaskList # Drag-drop enabled task list
├── DayCell          # Calendar day cell
└── MainWindow       # Main application window
```

## 📦 Dependencies

- **PyQt6** - GUI framework
- **requests** - Discord webhook integration

See `requirements.txt` for full list.

## 🐛 Troubleshooting

### GIFs not displaying
- Ensure bundled GIFs are in same directory as main.py
- For .exe builds, ensure `build_exe.bat` includes `--add-data` for GIFs

### Discord notifications not working
- Verify webhook URL is correct
- Check `reminders_enabled` setting
- Confirm network connectivity

### Tasks not saving
- Check disk space
- Verify write permissions for `tasks.json`
- Check file isn't corrupted (can restore from backup)

## 📝 License

© 2026 - All rights reserved. Custom use only.

This project is provided for personal and custom implementation use. For commercial use or redistribution, contact the author.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Use clear commit messages
4. Submit a pull request

## 👨‍💻 Author

**galmx (xdrew87)**
- GitHub: [@xdrew87](https://github.com/xdrew87)

## 🎨 Design

- **Theme**: Dark cyberpunk with neon accents (#00FF9C)
- **Font**: Consolas / Segoe UI
- **Color Palette**: Deep blues, neon green highlights, category-specific colors

## 🔮 Roadmap

Potential future features:
- [ ] Custom work hours/availability
- [ ] Task templates
- [ ] Pomodoro statistics
- [ ] Break timer
- [ ] Cloud sync
- [ ] Mobile app

## Support

For issues, feature requests, or questions:
1. Check existing GitHub issues
2. Create a detailed issue with reproduction steps
3. Include Python version and OS information

---

**Made with ❤️ for productivity.**
