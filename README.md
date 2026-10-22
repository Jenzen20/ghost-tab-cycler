# 👻 Ghost Tab Cycler

A completely **invisible** background app that automatically cycles through browser tabs with natural scrolling. Perfect for presentations where you need tabs to look actively browsed.

## ⚡ Quick Start

### First Time Setup (already done)
```
py -m venv venv
venv\Scripts\pip install -r requirements.txt
```

### Running the App
1. **Double-click** `START_GHOST.vbs` — the app starts completely hidden
2. You'll hear **3 ascending beeps** (confirmation it's running)
3. Open your browser with all the tabs you want
4. Press **`Ctrl+Alt+S`** to start cycling — you'll hear **2 high beeps**
5. Press **`Ctrl+Alt+S`** again to pause — you'll hear **1 low beep**
6. Press **`Ctrl+Alt+Q`** to quit — you'll hear **3 descending beeps**

### Emergency Stop
- Double-click `STOP_GHOST.vbs` to force-kill the app

---

## 🎯 What It Does

When cycling is **ON**, on each interval it:

| Step | Action | Purpose |
|------|--------|---------|
| 1 | `Ctrl+Tab` | Switch to the next browser tab |
| 2 | Scroll down ↓ | Simulate reading down the page |
| 3 | Pause (~2 sec) | Natural reading pause |
| 4 | Scroll up ↑ | Scroll back slightly |
| 5 | Wait (interval) | Wait before switching again |

Then it repeats from Step 1.

---

## ⚙️ Configuration

Edit `config.json` before launching:

```json
{
    "interval_seconds": 60,        // Time between each tab switch (default: 60s / 1 min)
    "scroll_down_amount": 3,       // How many scroll ticks down
    "scroll_up_amount": 3,         // How many scroll ticks up
    "scroll_delay": 0.8,           // Delay between scroll actions
    "pause_before_scroll_up": 2.0, // Pause after scrolling down (seconds)
    "pause_after_scroll_up": 1.0,  // Pause after scrolling up (seconds)
    "hotkey_toggle": "ctrl+alt+s", // Hotkey to start/stop cycling
    "hotkey_quit": "ctrl+alt+q"    // Hotkey to quit the app entirely
}
```

### Examples
- **Fast cycling (30 seconds):** set `"interval_seconds": 30`
- **Slower, more natural:** set `"interval_seconds": 90` with `"scroll_down_amount": 5`
- **Different hotkey:** set `"hotkey_toggle": "ctrl+shift+a"`

---

## 🔒 Why It's Invisible

| Layer | How |
|-------|-----|
| **No window** | Uses `pythonw.exe` (windowless Python) — no console, no GUI |
| **No taskbar icon** | No window = no taskbar entry |
| **No tray icon** | Nothing in system tray |
| **No screen capture** | Nothing to capture — only keyboard/mouse events are simulated |
| **Hidden launch** | VBScript launches with window style 0 (hidden) |

The app exists only as a background process. The only way to know it's running is through Task Manager (look for `pythonw.exe`).

---

## 🎵 Audio Feedback

Since the app is invisible, it uses **beep sounds** so you know what's happening:

| Sound | Meaning |
|-------|---------|
| 🔊 ↑↑↑ (3 ascending) | App started successfully |
| 🔊 ↑↑ (2 high beeps) | Cycling turned **ON** |
| 🔊 ↓ (1 low beep) | Cycling turned **OFF** |
| 🔊 ↓↓↓ (3 descending) | App quitting |

---

## 📁 Files

```
TRy app/
├── ghost_tab.py       ← Main app logic
├── config.json        ← Your settings (edit this!)
├── START_GHOST.vbs    ← Double-click to launch hidden
├── STOP_GHOST.vbs     ← Double-click to force-stop
├── requirements.txt   ← Python dependencies
└── venv/              ← Virtual environment (auto-created)
```
