# TradingView DOM Auto-Center Script

This script enhances the Desktop Version of TradingView by automating the centering of the Level 2 (Depth of Market, or DOM) view, a feature no longer natively supported. In fast-moving markets, manually scrolling or clicking the auto-center icon can be tedious. This Python-based system tray application solves this by automatically centering the DOM when active.

## Setup

### Prerequisites
- **Operating System**: Windows 11
- **Python Version**: Python 3.13

### Installation Steps
1. **Install Python 3.13**:
   - Download the latest Python 3.13 installer from [python.org](https://www.python.org/downloads/).
   - Run the installer, ensuring you check the box to "Add Python to PATH" during installation.
   - Verify installation by opening a Command Prompt and typing `python --version` (or `python3 --version` if `python` doesn't work). You should see `Python 3.13.x`.

2. **Install Dependencies**:
   - Clone this repository or download the script file.
   - Open a Command Prompt, navigate to the script's directory, and run:
     ```
     pip install -r requirements.txt
     ```
   - The `requirements.txt` file includes only the necessary packages: `pystray`, `pillow`, `pyautogui`, and `pynput`.

## Usage

1. **Run the Script**:
   - Open a Command Prompt, navigate to the script's directory, and run:
     ```
     python autocenter.py
     ```
   - Replace `autocenter.py` with the actual filename if different.

2. **System Tray Icon**:
   - A new icon will appear in your system tray. 
   ![System Tray Icon](screenshots/screenshot1.png)
   - Right-click the icon to open the menu. 
   ![Right-Click Menu](screenshots/screenshot2.png)

3. **Controls**:
   - Right-click to toggle "Auto-Centering" (activate/deactivate) or select "Exit" to stop the script.
   - **Icon States**:
     - **Red**: Auto-centering is deactivated.
     - **Orange**: Auto-centering is activated, but the script is not on a TradingView tab where DOM centering is applicable. 
     ![Orange Icon](screenshots/screenshot3.png)
     - **Green**: Auto-centering is activated and currently centering the DOM on an eligible TradingView tab. 
     ![Green Icon](screenshots/screenshot4.png)

## What the Script Does
The script monitors the active window for TradingView (detected by specific title keywords like "%", "+", or "−"). When enabled and focused on a compatible TradingView tab, it automatically sends the `Shift + Alt + C` key combination to center the DOM every 0.5–1.5 seconds, mimicking the manual auto-center action. It runs in the background via the system tray, updating its icon color to reflect its status.

## Notes
- Ensure TradingView is running and the DOM is visible for the script to function.
- The script uses keyboard and mouse input monitoring to avoid sending commands during user interaction.