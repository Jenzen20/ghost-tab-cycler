# 👻 Ghost Tab Cycler

A completely **invisible** background app that automatically cycles through browser tabs with natural, randomized scrolling. Perfect for presentations, monitors, or displays where you need browser tabs to look actively browsed.

---

## ⚡ Complete Beginner's Setup Guide

If you're starting on a brand new computer or have never used Python before, follow these step-by-step instructions:

---

### Step 1: Install Python (If you don't have it yet)

1. Open your browser and go to the official Python download page:  
   👉 **[https://www.python.org/downloads/](https://www.python.org/downloads/)**
2. Click the yellow button that says **"Download Python 3.x.x"**.
3. Open the downloaded setup file (e.g., `python-3.12.x-amd64.exe`).
4. ⚠️ **VERY IMPORTANT (DO NOT SKIP):**  
   At the very bottom of the first setup window, check the box:  
   ☑️ **"Add python.exe to PATH"**  
   *(If you miss this checkbox, Windows will not recognize Python commands!)*
5. Click **"Install Now"** and wait for it to finish.
6. Once finished, click **"Close"**.

> **How to verify Python is installed:**  
> Press `Win + R`, type `cmd`, press Enter, then type:  
> ```cmd
> py --version
> ```  
> If it displays Python 3.x.x, you are ready for the next step!

---

### Step 2: Set Up the Project

You can set up the app using either **Option A (Automatic)** or **Option B (Manual)**:

#### Option A: 1-Click Automatic Setup (Easiest)
1. In the project folder, locate **`setup.bat`**.
2. **Double-click `setup.bat`**.
3. It will automatically detect Python, create your virtual environment (`venv`), and install all necessary dependencies (`pynput`).
4. When you see `Setup Completed Successfully!`, press any key to close the window. Done!

---

#### Option B: Manual Setup via Terminal
If you prefer using the command line:

1. Open the project folder in File Explorer.
2. Click on the address bar at the top of the folder window, type `cmd` or `powershell`, and press **Enter**.
3. Create the isolated virtual environment:
   ```cmd
   py -m venv venv
   ```
4. Install the required dependencies:
   ```cmd
   venv\Scripts\pip install -r requirements.txt
   ```

---

## 🚀 How to Run and Use the App

1. **Open your browser** (Chrome, Edge, Firefox, Brave, etc.) and open all the tabs you want to cycle through.
2. **Double-click `START_GHOST.vbs`** in the project folder.  
   - The app runs completely invisible in the background (no black console window).
3. **Switch to your browser** within **3 seconds** (there is a 3-second grace period).
4. After 3 seconds, the app will **automatically start cycling** through your tabs and scrolling up and down naturally!

---

## ⌨️ Controls & Hotkeys

| Action | Default Hotkey | What It Does |
|--------|----------------|--------------|
| **Pause / Resume** | **`Ctrl + Pause`** *(or just **`Pause/Break`**)* | Temporarily pauses tab cycling so you can use your computer normally. Press again to resume. |
| **Quit App** | **`End`** | Completely shuts down and exits the background app. |
| **Emergency Stop** | **Double-click `STOP_GHOST.vbs`** | Instantly force-kills any running instance of the app if you can't reach the keyboard hotkey. |

> 💡 **Laptop or 60% keyboard without a Pause/Break key?**  
> You can easily change your toggle hotkey in `config.json`! For example, set `"hotkey_toggle": "ctrl+f1"` or `"hotkey_toggle": "ctrl+shift+s"`.

---

## 🎯 What It Does

When active, the app sends **`Ctrl+Tab`** to switch to the next tab, then simulates natural human browsing behavior using **10 randomized browsing patterns**:

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

You can customize the settings by opening **`config.json`** in Notepad or any text editor:

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
| `scroll_down_amount` | `6` | Base scroll down tick amount |
| `scroll_up_amount` | `4` | Base scroll up tick amount |
| `scroll_delay` | `0.8` | Delay between scroll steps |
| `pause_before_scroll_up` | `4.0` | Pause duration before scrolling back up |
| `pause_after_scroll_up` | `5.0` | Pause duration after scrolling back up |

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

The app exists strictly as a background process. The only place it can be seen is in Windows Task Manager (look for `pythonw.exe`).

---

## ❓ Troubleshooting & FAQs

### 1. `setup.bat` says "Python is not installed or not added to PATH"
You may have installed Python without checking the **"Add python.exe to PATH"** checkbox.  
**Fix:** Run the Python installer again, click **"Modify"**, make sure **"Add Python to environment variables"** is checked, and click **Install**.

### 2. "Virtual environment not found!" pop-up appears when clicking `START_GHOST.vbs`
You haven't run the first-time setup yet.  
**Fix:** Double-click **`setup.bat`** and let it finish, then double-click `START_GHOST.vbs` again.

### 3. How do I know if the app is currently running?
Open **Task Manager** (`Ctrl + Shift + Esc`) and look under **Background processes** for `pythonw.exe`.

### 4. How do I stop the app if my hotkeys don't work?
Double-click **`STOP_GHOST.vbs`** in the project folder. It will instantly terminate any running ghost process.

---

## 📁 Files Overview

```
ghost-tab-cycler/
├── setup.bat          ← 1-Click setup script for beginners
├── START_GHOST.vbs    ← Double-click to launch the app hidden
├── STOP_GHOST.vbs     ← Double-click to force-quit the app
├── config.json        ← Configurable settings & hotkeys
├── ghost_tab.py       ← Main app logic with 10 randomized patterns
├── requirements.txt   ← Python dependencies (pynput)
└── venv/              ← Virtual environment (created by setup)
```
