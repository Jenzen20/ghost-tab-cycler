# 👻 Ghost Tab Cycler

A completely **invisible** background app that automatically cycles through browser tabs with natural, randomized scrolling. Perfect for presentations or displays where you need tabs to look actively browsed.

## ⚡ Quick Start

### First Time Setup (already done)
```powershell
py -m venv venv
venv\Scripts\pip install -r requirements.txt
```

### Running the App
1. Open your browser with all the tabs you want to cycle through.
2. **Double-click** `START_GHOST.vbs` — the app starts completely hidden.
3. After an initial **3-second grace period**, tab cycling begins **automatically**.
4. Press **`Ctrl+Pause`** (or just the **`Pause/Break`** key) to pause or resume cycling.
5. Press **`End`** to quit the app completely.

### Emergency Stop
- Double-click `STOP_GHOST.vbs` to force-kill the app, or press the **`End`** hotkey.

---

## 🎯 What It Does

When cycling is active, the app sends **`Ctrl+Tab`** to switch to the next tab, then simulates natural human browsing behavior using **10 randomized browsing patterns**:

| Pattern | Behavior |
|---------|----------|
| **Simple** | Standard scroll down, natural pause, slight scroll back up |
| **Deep Read** | Deeper scroll down with longer reading pause |
| **Skim** | Quick scroll down and up |
| **Scroll & Pause & Scroll** | Two-phase reading with an intermediate pause |
| **Back & Forth** | Multiple passes reading back and forth |
| **Gradual** | Incremental step-by-step reading down the page |
| **Burst Read** | Rapid scroll followed by focused pause |
| **Deep Dive** | Extended scroll down with slow, thorough review |
| **Casual Glance** | Light scroll down and quick check |
| **Explorer** | Multiple segmented chunks down the page |

Every cycle also randomizes scroll speeds (`fast`, `normal`, `slow`, `lazy`), scroll distance, and delay times (between 3 to 7 seconds between tab switches) so the browsing activity looks organic and never robotic.

---

## ⚙️ Configuration

Edit `config.json` before launching:

```json
{
    "start_active": true,
    "interval_seconds": 0,
    "scroll_down_amount": 6,
    "scroll_up_amount": 4,
    "scroll_delay": 0.8,
    "pause_before_scroll_up": 4.0,
    "pause_after_scroll_up": 5.0,
    "hotkey_toggle": "ctrl+pause",
    "hotkey_quit": "end"
}
```

### Settings Explained

| Setting | Default | Description |
|---------|---------|-------------|
| `start_active` | `true` | When `true`, automatically begins cycling 3 seconds after launch |
| `hotkey_toggle` | `"ctrl+pause"` | Hotkey to pause / resume cycling (also triggered by `Pause/Break` key) |
| `hotkey_quit` | `"end"` | Hotkey to completely exit the background app |
| `interval_seconds` | `0` | Base interval setting |
| `scroll_down_amount` | `6` | Scroll down tick amount |
| `scroll_up_amount` | `4` | Scroll up tick amount |
| `scroll_delay` | `0.8` | Delay between scroll steps |
| `pause_before_scroll_up` | `4.0` | Pause duration before scrolling back up |
| `pause_after_scroll_up` | `5.0` | Pause duration after scrolling back up |

---

## ⌨️ Hotkeys & Controls

| Action | Default Hotkey | Details |
|--------|----------------|---------|
| **Pause / Resume** | `Ctrl+Pause` or `Pause` | Toggles tab cycling ON and OFF without closing the app |
| **Quit App** | `End` | Terminates the background process cleanly |
| **Force Stop** | `STOP_GHOST.vbs` | Double-click if you want to force-kill the process |

---

## 🔒 Why It's Invisible & Silent

| Layer | How |
|-------|-----|
| **Completely Silent** | No beeps or audio alerts — runs in total silence |
| **No window** | Uses `pythonw.exe` (windowless Python) — no console, no GUI |
| **No taskbar icon** | No window = no taskbar entry |
| **No tray icon** | Nothing in system tray |
| **No screen capture** | Nothing to capture — only keyboard/mouse events are simulated |
| **Hidden launch** | VBScript launches with window style 0 (hidden) |
| **Single Instance** | Uses a Windows Named Mutex to prevent multiple copies running at once |

The app exists strictly as a background process. The only way to see it is via Task Manager (look for `pythonw.exe`).

---

## 📁 Files

```
TRy app/
├── ghost_tab.py       ← Main app logic with 10 randomized browsing patterns
├── config.json        ← Your settings (hotkeys, active state)
├── START_GHOST.vbs    ← Double-click to launch hidden
├── STOP_GHOST.vbs     ← Double-click to force-stop
├── requirements.txt   ← Python dependencies (pynput)
└── venv/              ← Virtual environment
```
