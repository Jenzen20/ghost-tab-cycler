"""
Ghost Tab Cycler - Hidden Background Auto Tab Cycler
=====================================================
A completely invisible background app that automatically cycles through
browser tabs with natural scrolling behavior. Controlled entirely via hotkeys.

No window, no taskbar icon, no tray icon - completely invisible.
Won't appear in screenshots or screen recordings since there's no UI.

Hotkeys (configurable in config.json):
  Pause/Break  →  Toggle cycling ON/OFF (start, pause, resume)
  End          →  Quit app completely

Behavior when ON:
  1. Sends Ctrl+Tab (switch to next browser tab)
  2. Scrolls down a small amount
  3. Pauses briefly
  4. Scrolls back up a small amount
  5. Waits for the configured interval
  6. Repeats from step 1
"""

import json
import time
import threading
import sys
import ctypes
from ctypes import wintypes
from pathlib import Path
from pynput.keyboard import Key, Listener, KeyCode


# ─── Windows API for reliable key/mouse simulation ──────────────────────────

user32 = ctypes.windll.user32

# Input event types
INPUT_KEYBOARD = 1
INPUT_MOUSE = 2

# Key event flags
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_EXTENDEDKEY = 0x0001

# Mouse event flags
MOUSEEVENTF_WHEEL = 0x0800

# Virtual key codes
VK_CONTROL = 0x11
VK_TAB = 0x09

WHEEL_DELTA = 120  # Standard scroll amount per "click"


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("union", INPUT_UNION),
    ]


def send_key_down(vk_code):
    """Press a key down using Windows SendInput API."""
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp.union.ki.wVk = vk_code
    inp.union.ki.dwFlags = 0
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))


def send_key_up(vk_code):
    """Release a key using Windows SendInput API."""
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp.union.ki.wVk = vk_code
    inp.union.ki.dwFlags = KEYEVENTF_KEYUP
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))


def send_ctrl_tab():
    """Send Ctrl+Tab keystroke to switch browser tab."""
    send_key_down(VK_CONTROL)
    time.sleep(0.05)
    send_key_down(VK_TAB)
    time.sleep(0.05)
    send_key_up(VK_TAB)
    time.sleep(0.05)
    send_key_up(VK_CONTROL)


def send_scroll(clicks):
    """
    Scroll the mouse wheel using mouse_event API.
    Positive clicks = scroll UP, negative clicks = scroll DOWN.
    """
    MOUSEEVENTF_WHEEL = 0x0800
    amount = clicks * WHEEL_DELTA
    # mouse_event handles signed scroll values correctly
    user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, ctypes.c_long(amount), 0)



# ─── Configuration ───────────────────────────────────────────────────────────

def load_config():
    """Load configuration from config.json in the same directory as this script."""
    config_path = Path(__file__).parent / "config.json"

    defaults = {
        "interval_seconds": 10,
        "scroll_down_amount": 3,
        "scroll_up_amount": 3,
        "scroll_delay": 0.8,
        "pause_before_scroll_up": 4.0,
        "pause_after_scroll_up": 1.0,
        "hotkey_toggle": "ctrl+pause",
        "hotkey_quit": "end",
        "start_active": True,
    }

    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                user_config = json.load(f)
            defaults.update(user_config)
        except Exception:
            pass  # Silently use defaults

    return defaults


def parse_hotkey(hotkey_str):
    """Parse a hotkey string like 'ctrl+alt+s' into a frozenset of pynput keys."""
    key_map = {
        "ctrl": Key.ctrl_l,
        "alt": Key.alt_l,
        "shift": Key.shift_l,
    }

    keys = set()
    for part in hotkey_str.lower().split("+"):
        part = part.strip()
        if part in key_map:
            keys.add(key_map[part])
        elif len(part) == 1:
            keys.add(KeyCode.from_char(part))
        else:
            # Try as Key attribute (e.g., 'pause', 'end', 'scroll_lock')
            try:
                keys.add(getattr(Key, part))
            except AttributeError:
                pass

    return frozenset(keys)


# ─── Global State ────────────────────────────────────────────────────────────

config = load_config()

cycling_active = config.get("start_active", True)  # Start cycling automatically if True
app_running = True          # Whether the entire app is alive
current_keys = set()        # Currently pressed keys
lock = threading.Lock()     # Thread safety for state changes

hotkey_toggle = parse_hotkey(config.get("hotkey_toggle", "ctrl+pause"))
hotkey_quit = parse_hotkey(config.get("hotkey_quit", "end"))




# ─── Tab Cycling Logic ──────────────────────────────────────────────────────

import random

def interruptible_sleep(seconds):
    """Sleep that can be interrupted when cycling is toggled off or app quits."""
    end_time = time.time() + seconds
    while time.time() < end_time:
        if not cycling_active or not app_running:
            return False
        time.sleep(0.25)
    return True


def do_scroll_down_ticks(amount, speed="normal"):
    """Scroll down one tick at a time with variable speed."""
    speed_ranges = {
        "fast":   (0.05, 0.12),
        "normal": (0.12, 0.25),
        "slow":   (0.25, 0.45),
        "lazy":   (0.40, 0.80),
    }
    lo, hi = speed_ranges.get(speed, (0.12, 0.25))
    for _ in range(amount):
        if not cycling_active or not app_running:
            return False
        send_scroll(-1)
        time.sleep(random.uniform(lo, hi))
    return True


def do_scroll_up_ticks(amount, speed="normal"):
    """Scroll up one tick at a time with variable speed."""
    speed_ranges = {
        "fast":   (0.05, 0.12),
        "normal": (0.12, 0.25),
        "slow":   (0.25, 0.45),
        "lazy":   (0.40, 0.80),
    }
    lo, hi = speed_ranges.get(speed, (0.12, 0.25))
    for _ in range(amount):
        if not cycling_active or not app_running:
            return False
        send_scroll(1)
        time.sleep(random.uniform(lo, hi))
    return True


def perform_cycle():
    """
    Execute one tab cycle with RANDOMIZED behavior.
    10 patterns x random scroll/speed/pause = thousands of unique combos.
    """

    # Random params for this cycle
    down_speed  = random.choice(["fast", "normal", "normal", "slow", "lazy"])
    up_speed    = random.choice(["fast", "fast", "normal", "slow"])
    pre_switch  = random.uniform(0.1, 0.5)
    post_switch = random.uniform(0.4, 1.2)
    wait_after  = random.uniform(3.0, 7.0)

    # Pick a random browsing pattern
    pattern = random.choices(
        population=[
            "simple",
            "deep_read",
            "skim",
            "scroll_pause_scroll",
            "back_and_forth",
            "gradual",
            "burst_read",
            "deep_dive",
            "casual_glance",
            "explorer",
        ],
        weights=[15, 12, 12, 10, 10, 10, 8, 8, 8, 7],
        k=1
    )[0]

    # Step 1: Switch tab
    time.sleep(pre_switch)
    send_ctrl_tab()
    time.sleep(post_switch)

    if not cycling_active or not app_running:
        return

    # Step 2: Execute the chosen pattern

    if pattern == "simple":
        scroll_down = random.randint(3, 10)
        scroll_up = random.randint(2, min(scroll_down, 7))
        if not do_scroll_down_ticks(scroll_down, down_speed):
            return
        if not interruptible_sleep(random.uniform(1.5, 6.0)):
            return
        if not do_scroll_up_ticks(scroll_up, up_speed):
            return

    elif pattern == "deep_read":
        if not do_scroll_down_ticks(random.randint(7, 14), random.choice(["normal", "slow"])):
            return
        if not interruptible_sleep(random.uniform(4.0, 8.0)):
            return
        if not do_scroll_up_ticks(random.randint(1, 3), "fast"):
            return

    elif pattern == "skim":
        if not do_scroll_down_ticks(random.randint(4, 8), "fast"):
            return
        if not interruptible_sleep(random.uniform(0.8, 2.0)):
            return
        if not do_scroll_up_ticks(random.randint(2, 5), "fast"):
            return

    elif pattern == "scroll_pause_scroll":
        first_down = random.randint(2, 5)
        second_down = random.randint(2, 5)
        if not do_scroll_down_ticks(first_down, down_speed):
            return
        if not interruptible_sleep(random.uniform(1.0, 3.0)):
            return
        if not do_scroll_down_ticks(second_down, down_speed):
            return
        if not interruptible_sleep(random.uniform(1.5, 4.0)):
            return
        if not do_scroll_up_ticks(random.randint(2, first_down + second_down - 1), up_speed):
            return

    elif pattern == "back_and_forth":
        for _ in range(random.randint(2, 3)):
            if not do_scroll_down_ticks(random.randint(2, 5), down_speed):
                return
            if not interruptible_sleep(random.uniform(0.8, 2.5)):
                return
            if not do_scroll_up_ticks(random.randint(1, 3), up_speed):
                return
            if not interruptible_sleep(random.uniform(0.5, 1.5)):
                return

    elif pattern == "gradual":
        total_down = random.randint(6, 12)
        for _ in range(total_down):
            if not cycling_active or not app_running:
                return
            send_scroll(-1)
            time.sleep(random.uniform(0.3, 0.9))
        if not interruptible_sleep(random.uniform(1.5, 3.5)):
            return
        if not do_scroll_up_ticks(random.randint(2, total_down // 2), up_speed):
            return

    elif pattern == "burst_read":
        if not do_scroll_down_ticks(random.randint(4, 8), "fast"):
            return
        if not interruptible_sleep(random.uniform(4.0, 8.0)):
            return
        if not do_scroll_up_ticks(random.randint(2, 4), "fast"):
            return

    elif pattern == "deep_dive":
        if not do_scroll_down_ticks(random.randint(8, 15), random.choice(["normal", "slow"])):
            return
        if not interruptible_sleep(random.uniform(3.0, 7.0)):
            return
        if not do_scroll_up_ticks(random.randint(1, 4), random.choice(["normal", "fast"])):
            return

    elif pattern == "casual_glance":
        if not do_scroll_down_ticks(random.randint(1, 3), random.choice(["fast", "normal"])):
            return
        if not interruptible_sleep(random.uniform(0.5, 2.0)):
            return
        if not do_scroll_up_ticks(random.randint(1, 2), "fast"):
            return

    elif pattern == "explorer":
        total_down = 0
        for _ in range(random.randint(2, 4)):
            chunk = random.randint(2, 4)
            total_down += chunk
            if not do_scroll_down_ticks(chunk, random.choice(["normal", "slow"])):
                return
            if not interruptible_sleep(random.uniform(1.0, 3.0)):
                return
        if not do_scroll_up_ticks(random.randint(2, max(2, total_down // 2)), up_speed):
            return

    # Step 3: Wait before next tab switch
    if not interruptible_sleep(wait_after):
        return


def cycling_loop():
    """Main loop that runs tab cycling with randomized patterns."""
    global cycling_active

    # Initial grace period when starting active (3 seconds to click Chrome)
    if cycling_active:
        time.sleep(3)

    while app_running:
        if cycling_active:
            perform_cycle()
        else:
            time.sleep(0.3)



# ─── Hotkey Handling ─────────────────────────────────────────────────────────

def normalize_key(key):
    """Normalize key variants (e.g., ctrl_r → ctrl_l) for consistent matching."""
    key_normalize_map = {
        Key.ctrl_r: Key.ctrl_l,
        Key.alt_r: Key.alt_l,
        Key.alt_gr: Key.alt_l,
        Key.shift_r: Key.shift_l,
    }
    # Windows converts Ctrl+Pause / Break into VK_CANCEL (vk=3) or VK_PAUSE (vk=19)
    if hasattr(key, 'vk') and key.vk in (3, 19):
        return Key.pause
    return key_normalize_map.get(key, key)


def on_press(key):
    """Handle key press events."""
    global cycling_active, app_running

    normalized = normalize_key(key)
    current_keys.add(normalized)

    # Also add the character key if it's a KeyCode with a char
    if hasattr(key, 'char') and key.char:
        current_keys.add(KeyCode.from_char(key.char.lower()))

    # Check toggle hotkey (triggers on Ctrl+Pause OR pressing Pause/Break directly)
    is_toggle = False
    if hotkey_toggle.issubset(current_keys):
        is_toggle = True
    elif normalized == Key.pause:
        is_toggle = True

    if is_toggle:
        with lock:
            cycling_active = not cycling_active
        current_keys.clear()

    # Check quit hotkey
    elif hotkey_quit.issubset(current_keys):
        with lock:
            cycling_active = False
            app_running = False
        current_keys.clear()
        return False  # Stop listener → app exits


def on_release(key):
    """Handle key release events."""
    normalized = normalize_key(key)
    current_keys.discard(normalized)

    if hasattr(key, 'char') and key.char:
        current_keys.discard(KeyCode.from_char(key.char.lower()))


# ─── Entry Point ─────────────────────────────────────────────────────────────

def main():
    """Start the ghost tab cycler."""
    global app_running

    # Enforce single instance using Windows Named Mutex
    ERROR_ALREADY_EXISTS = 183
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "GhostTabCyclerSingleInstanceMutex")
    if ctypes.windll.kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        sys.exit(0)

    # Start the cycling thread
    cycle_thread = threading.Thread(target=cycling_loop, daemon=True)
    cycle_thread.start()

    # Listen for hotkeys (blocks until quit hotkey is pressed)
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # Cleanup
    app_running = False
    cycle_thread.join(timeout=2)


if __name__ == "__main__":
    main()
