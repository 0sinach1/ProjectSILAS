import pyautogui
import subprocess
import webbrowser
import os

# Safety setting — move mouse to corner to abort if something goes wrong
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# ── App Control ───────────────────────────────────
def open_app(app_name):
    """Open an application by name"""
    apps = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "firefox": "firefox",
        "notepad": "notepad",
        "vscode": "code",
        "explorer": "explorer",
        "calculator": "calc",
        "spotify": "spotify",
        "discord": "discord",
        "whatsapp": "whatsapp",
        "terminal": "cmd",
    }

    app = apps.get(app_name.lower())

    if app:
        try:
            subprocess.Popen(app)
            return True
        except Exception as e:
            print(f"Could not open {app_name}: {e}")
            return False
    else:
        # Try opening it directly by name as a last resort
        try:
            subprocess.Popen(app_name)
            return True
        except:
            return False

# ── Screenshot ────────────────────────────────────
def take_screenshot():
    """Take a screenshot and save it to desktop"""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filepath = os.path.join(desktop, "silas_screenshot.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"Screenshot saved to {filepath}")
    return filepath

# ── Browser Tab Control ───────────────────────────
def change_tab():
    """Switch to next browser tab"""
    pyautogui.hotkey('ctrl', 'tab')

def close_tab():
    """Close current browser tab"""
    pyautogui.hotkey('ctrl', 'w')

def new_tab():
    """Open a new browser tab"""
    pyautogui.hotkey('ctrl', 't')

# ── Volume Control ────────────────────────────────
def volume_up():
    """Increase system volume"""
    for _ in range(5):
        pyautogui.hotkey('volumeup')

def volume_down():
    """Decrease system volume"""
    for _ in range(5):
        pyautogui.hotkey('volumedown')

def mute():
    """Mute or unmute system volume"""
    pyautogui.hotkey('volumemute')

# ── Scrolling ─────────────────────────────────────
def scroll_up():
    """Scroll up"""
    pyautogui.scroll(5)

def scroll_down():
    """Scroll down"""
    pyautogui.scroll(-5)

# ── Web Search ────────────────────────────────────
def search_web(query):
    """Open browser and search for query"""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    print(f"Searching for: {query}")

# ── Window Control ────────────────────────────────
def minimize_window():
    """Minimize current window"""
    pyautogui.hotkey('win', 'down')

def maximize_window():
    """Maximize current window"""
    pyautogui.hotkey('win', 'up')

# ── Clipboard ─────────────────────────────────────
def read_clipboard():
    """Read current clipboard content"""
    import pyperclip
    content = pyperclip.paste()
    return content

def type_text(text):
    """Type text at current cursor position"""
    pyautogui.typewrite(text, interval=0.05)

# ── Action Router ─────────────────────────────────
def execute(action, params):
    """Routes the action name to the right function"""
    if action == "open_app":
        return open_app(params.get("app_name", ""))

    elif action == "take_screenshot":
        return take_screenshot()

    elif action == "change_tab":
        return change_tab()

    elif action == "volume_up":
        return volume_up()

    elif action == "volume_down":
        return volume_down()

    elif action == "mute":
        return mute()

    elif action == "scroll_up":
        return scroll_up()

    elif action == "scroll_down":
        return scroll_down()

    elif action == "search_web":
        return search_web(params.get("query", ""))

    elif action == "minimize_window":
        return minimize_window()

    elif action == "maximize_window":
        return maximize_window()

    elif action == "read_clipboard":
        return read_clipboard()

    elif action == "type_text":
        return type_text(params.get("text", ""))

    elif action == "answer_question":
        pass  # No laptop action needed, just speak

    else:
        print(f"Unknown action: {action}")