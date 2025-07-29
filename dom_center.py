import pystray
from PIL import Image, ImageDraw
import pyautogui
import ctypes
import time
import random
import threading
import logging
from pynput import keyboard, mouse

# Setup logging to file for debugging
# logging.basicConfig(filename='autocenter.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Define key combination and title keywords for TradingView
KEY_COMBINATION = ('shift', 'alt', 'c')
TITLE_KEYWORDS_AND = ["%"]
TITLE_KEYWORDS_OR = ["+", "−"]

# Global flags to control the application
enabled = False
running = True

# Define colors for the icons
ENABLED_COLOR = (50, 205, 50)  # Lime green
DISABLED_COLOR = (220, 20, 60)  # Crimson red
ORANGE_COLOR = (255, 165, 0)  # Orange

def create_icon(color):
    """Create an icon with a colored circle and white border on black background."""
    image = Image.new('RGB', (64, 64), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((12, 12, 52, 52), fill=None, outline=(255, 255, 255), width=2)
    draw.ellipse((16, 16, 48, 48), fill=color)
    return image

# Create the icons
enabled_icon = create_icon(ENABLED_COLOR)
disabled_icon = create_icon(DISABLED_COLOR)
orange_icon = create_icon(ORANGE_COLOR)

def is_tradingview_window():
    """Check if the active window is TradingView based on title keywords."""
    try:
        handle = ctypes.windll.user32.GetForegroundWindow()
        length = ctypes.windll.user32.GetWindowTextLengthW(handle)
        buffer = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(handle, buffer, length + 1)
        title = buffer.value.lower()
        
        # Check that ALL keywords from TITLE_KEYWORDS_AND are present
        and_match = all(keyword.lower() in title for keyword in TITLE_KEYWORDS_AND)
        
        # Check that at least ONE keyword from TITLE_KEYWORDS_OR is present
        or_match = any(keyword.lower() in title for keyword in TITLE_KEYWORDS_OR)
        
        is_match = and_match and or_match
        logging.debug(f"Current window: {buffer.value}, Is TradingView: {is_match}")
        return is_match
    except Exception as e:
        logging.error(f"Error getting window title: {e}")
        return False

def send_key_combination():
    """Send the Shift + Alt + C key combination."""
    try:
        pyautogui.hotkey(*KEY_COMBINATION)
        logging.debug("Sent Shift + Alt + C to TradingView")
    except Exception as e:
        logging.error(f"Error sending key combination: {e}")

# Sets to track currently pressed keys and mouse buttons
pressed_keys = set()
pressed_mouse_buttons = set()

# Global variables for listeners
keyboard_listener = None
mouse_listener = None

# Callback functions for pynput listeners
def on_press(key):
    pressed_keys.add(key)

def on_release(key):
    pressed_keys.discard(key)

def on_click(x, y, button, pressed):
    if pressed:
        pressed_mouse_buttons.add(button)
    else:
        pressed_mouse_buttons.discard(button)

def autocenter_thread():
    """Thread that periodically triggers the key combination when enabled and updates the icon."""
    while running:
        if not enabled:
            icon.icon = disabled_icon
            time.sleep(0.1)
            continue
        in_focus = is_tradingview_window()
        icon.icon = enabled_icon if in_focus else orange_icon
        if in_focus and not pressed_keys and not pressed_mouse_buttons:
            send_key_combination()
        time.sleep(random.uniform(0.5, 1.5))

def toggle_autocenter(icon, item):
    """Toggle the auto-centering feature and update the icon immediately."""
    global enabled
    enabled = not enabled
    logging.debug(f"Auto-centering {'enabled' if enabled else 'disabled'}")
    if not enabled:
        icon.icon = disabled_icon
    else:
        in_focus = is_tradingview_window()
        icon.icon = enabled_icon if in_focus else orange_icon

def exit_app(icon, item):
    """Exit the application."""
    global running
    keyboard_listener.stop()
    mouse_listener.stop()
    running = False
    icon.stop()

def setup(icon):
    """Initialize the system tray icon, start listeners, and the auto-centering thread."""
    icon.visible = True
    global keyboard_listener, mouse_listener
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener.start()
    mouse_listener.start()
    thread = threading.Thread(target=autocenter_thread, daemon=True)
    thread.start()

def create_menu():
    """Create the system tray menu with a checkable item for auto-centering."""
    return pystray.Menu(
        pystray.MenuItem("Auto-Centering", toggle_autocenter, checked=lambda item: enabled),
        pystray.MenuItem("Exit", exit_app)
    )

# Create and run the system tray icon with the initial disabled icon
icon = pystray.Icon("TradingView DOM Auto-Center", disabled_icon, "TradingView DOM Auto-Center", menu=create_menu())
icon.run(setup)