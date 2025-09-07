## Autoclicker by Lim

A minimal, dark-themed Windows auto-clicker built with Tkinter and PyAutoGUI. Set a click delay, choose the mouse button, and start/stop clicking via UI or a global hotkey.

### Features
- **Simple UI**: Set delay in seconds and choose left/right click
- **Global hotkey**: Optional F6 toggles Start/Stop (via `keyboard`)
- **Threaded clicking**: Smooth UI while clicking in the background
- **Dark mode**: Dark title bar on supported Windows builds
- **Tray-friendly**: Window is small and non-resizable

### Download
- Grab the single EXE from the Releases page and run it directly. If Windows SmartScreen appears, click “More info” → “Run anyway”.

### Requirements (for running from source)
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
Artifacts are created under `dist/` and `build/`. The icon is set to `icon/acbl.ico` and a PNG `icon/acbl.png` is bundled for the taskbar/title icon.

If you prefer a one-liner without the spec (defaults may differ), you can also run:
```bash
pyinstaller --onefile --noconsole --name "autoclicker by Lim" --icon icon/acbl.ico autoclicker.py
```

### Clean rebuild
```bash
# From repo root
# Remove prior outputs then build with the spec
rm -r -fo build dist 2>$null | out-null
pyinstaller "autoclicker by Lim.spec"
```

### Troubleshooting
- **Hotkey F6 not working**: Ensure `keyboard` is installed and the app is run as Administrator, or disable hotkeys in the UI.
- **Clicks not registering in some apps**: Some games/applications block synthetic input. Try running as Administrator.
- **Taskbar/title icon shows default (feather)**: Ensure `icon/acbl.ico` includes multiple sizes and that `icon/acbl.png` exists; rebuild cleanly. If Windows caches the old icon, rename the EXE or run `ie4uinit.exe -ClearIconCache`.
- **Display scaling or multiple monitors**: PyAutoGUI uses screen coordinates; unusual DPI settings or virtual desktops may affect behavior.

### Project structure
- `autoclicker.py`: Main application
- `autoclicker by Lim.spec`: PyInstaller build spec
- `installer.iss`: Optional Windows installer script
- `icon/acbl.ico`, `icon/acbl.png`: App icons

### License
MIT

### Acknowledgments
- Built with `tkinter`, `pyautogui`, and optional `keyboard` for global hotkeys.
