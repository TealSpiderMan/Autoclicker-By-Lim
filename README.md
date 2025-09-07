## Autoclicker by Lim

A minimal, dark-themed Windows auto-clicker built with Tkinter and PyAutoGUI. Set a click delay, choose the mouse button, and start/stop clicking via UI or a global hotkey.

### Features
- **Simple UI**: Set delay in seconds and choose left/right click
- **Global hotkey**: Optional F6 toggles Start/Stop (via `keyboard`)
- **Threaded clicking**: Smooth UI while clicking in the background
- **Dark mode**: Dark title bar on supported Windows builds
- **Tray-friendly**: Window is small and non-resizable

### Requirements
- **OS**: Windows 10/11
- **Python**: 3.10+
- **Packages**:
  - `pyautogui`
  - `keyboard` (optional; enables the F6 global hotkey)
  - `tkinter` (bundled with standard Python on Windows)

Install packages:
```bash
pip install pyautogui keyboard
```

Note: The `keyboard` library may need administrator privileges to register global hotkeys on Windows. If hotkeys do not work, run the app as Administrator or uncheck the hotkey option and use the UI buttons.

### Run from source
```bash
python autoclicker.py
```

### Usage
1. Enter the delay between clicks in seconds (e.g., `0.1`).
2. Choose the mouse button: Left or Right.
3. Click Start to begin clicking; Stop to halt.
4. If enabled, press **F6** anytime to toggle Start/Stop globally.

Notes:
- Delay must be a positive number.
- While running, the app shows status and disables Start to prevent duplicates.

### Build a Windows executable (PyInstaller)
This repo includes a PyInstaller spec: `autoclicker by Lim.spec`. Build with:
```bash
pyinstaller "autoclicker by Lim.spec"
```
Artifacts are created under `dist/` and `build/`. The icon is set to `icon/acbl.ico` via the spec. If you customize paths, update the spec accordingly.

If you prefer a one-liner without the spec (defaults may differ), you can also run:
```bash
pyinstaller --noconsole --name "autoclicker by Lim" --icon icon/acbl.ico autoclicker.py
```

### Troubleshooting
- **Hotkey F6 not working**: Ensure `keyboard` is installed and the app is run as Administrator, or disable hotkeys in the UI.
- **Clicks not registering in some apps**: Some games/applications block synthetic input. Try running as Administrator.
- **Display scaling or multiple monitors**: PyAutoGUI uses screen coordinates; unusual DPI settings or virtual desktops may affect behavior.

### Project structure
- `autoclicker.py`: Main application
- `autoclicker by Lim.spec`: PyInstaller build spec
- `icon/acbl.ico`: App icon used for the window and build

### License
MIT

### Acknowledgments
- Built with `tkinter`, `pyautogui`, and optional `keyboard` for global hotkeys.
