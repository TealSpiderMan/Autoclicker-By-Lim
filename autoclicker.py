import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import ctypes

import pyautogui
try:
	import keyboard  # Global hotkeys
except Exception:
	keyboard = None  # type: ignore[assignment]


class AutoClickerApp:
	def __init__(self, root: tk.Tk) -> None:
		self.root = root
		self.root.title("autoclicker by Lim")
		self.root.resizable(False, False)
		self.root.configure(bg="#000000")
		# Remove any white focus border around the root window
		try:
			self.root.configure(highlightthickness=0)
		except Exception:
			pass
		# Window opacity (0.0 fully transparent - 1.0 opaque)
		try:
			self.root.attributes("-alpha", 1.0)
		except Exception:
			pass

		# Try enabling dark title bar on Windows (immersive dark mode)
		self._enable_win_dark_titlebar()

		self.is_running = False
		self.stop_event = threading.Event()
		self.worker_thread: threading.Thread | None = None

		self.delay_var = tk.StringVar(value="0.1")
		self.button_var = tk.StringVar(value="left")
		self.status_var = tk.StringVar(value="Idle")
		self.enable_hotkeys_var = tk.BooleanVar(value=keyboard is not None)
		self._hotkey_handles: list[int] = []

		# Shared style (dark theme)
		self.style = ttk.Style()
		try:
			self.style.theme_use("clam")
		except Exception:
			# Fallback to a dark-friendlier built-in if clam unavailable
			for fallback in ("alt", "default"):
				try:
					self.style.theme_use(fallback)
					break
				except Exception:
					continue
		font_main = ("Segoe UI", 12)
		font_large = ("Segoe UI", 13)
		self.style.configure("Dark.TFrame", background="#000000")
		self.style.configure("Dark.TLabel", background="#000000", foreground="#FFFFFF", font=font_main)
		self.style.configure("Dark.TButton", background="#222222", foreground="#FFFFFF", font=font_large)
		self.style.map("Dark.TButton", background=[("active", "#333333")])
		self.style.configure("Dark.TRadiobutton", background="#000000", foreground="#FFFFFF", font=font_main)
		self.style.map("Dark.TRadiobutton", background=[("active", "#111111"), ("!active", "#000000")])
		# Dedicated dark style for ttk.Checkbutton (avoid white background on some themes)
		self.style.configure("Dark.TCheckbutton", background="#000000", foreground="#FFFFFF", font=font_main)
		self.style.map("Dark.TCheckbutton", background=[("active", "#111111"), ("!active", "#000000")])
		# Entry field background supported by clam theme
		self.style.configure("Dark.TEntry", fieldbackground="#111111", foreground="#FFFFFF", insertcolor="#FFFFFF", selectbackground="#444444", selectforeground="#FFFFFF")

		self._build_ui()
		self.root.protocol("WM_DELETE_WINDOW", self._on_close)
		# Register hotkeys if available and enabled
		self._maybe_register_hotkeys()

	def _build_ui(self) -> None:
		container = ttk.Frame(self.root, padding=16, style="Dark.TFrame")
		container.grid(row=0, column=0, sticky="nsew")

		# Delay input
		delay_label = ttk.Label(container, text="Delay (seconds between clicks):", style="Dark.TLabel")
		delay_label.grid(row=0, column=0, sticky="w", pady=(0, 6))
		delay_entry = ttk.Entry(container, textvariable=self.delay_var, width=14, style="Dark.TEntry")
		delay_entry.grid(row=0, column=1, padx=(8, 0), sticky="w")

		# Button selection
		btn_label = ttk.Label(container, text="Mouse button:", style="Dark.TLabel")
		btn_label.grid(row=1, column=0, sticky="w", pady=(8, 0))
		btn_frame = ttk.Frame(container, style="Dark.TFrame")
		btn_frame.grid(row=1, column=1, padx=(8, 0), sticky="w", pady=(8, 0))
		left_radio = ttk.Radiobutton(btn_frame, text="Left", value="left", variable=self.button_var, style="Dark.TRadiobutton")
		right_radio = ttk.Radiobutton(btn_frame, text="Right", value="right", variable=self.button_var, style="Dark.TRadiobutton")
		left_radio.grid(row=0, column=0, sticky="w")
		right_radio.grid(row=0, column=1, padx=(8, 0), sticky="w")

		# Controls
		controls = ttk.Frame(container, style="Dark.TFrame")
		controls.grid(row=2, column=0, columnspan=2, pady=(12, 0), sticky="w")
		self.start_btn = ttk.Button(controls, text="Start", command=self.start_clicking, style="Dark.TButton")
		self.stop_btn = ttk.Button(controls, text="Stop", command=self.stop_clicking, state=tk.DISABLED, style="Dark.TButton")
		self.start_btn.grid(row=0, column=0, sticky="w")
		self.stop_btn.grid(row=0, column=1, padx=(8, 0), sticky="w")

		# Hotkeys toggle
		hotkeys_frame = ttk.Frame(container, style="Dark.TFrame")
		hotkeys_frame.grid(row=3, column=0, columnspan=2, pady=(12, 0), sticky="w")
		hotkeys_label_text = "Enable global hotkey (F6 toggles Start/Stop)"
		self.hotkeys_check = ttk.Checkbutton(
			hotkeys_frame,
			text=hotkeys_label_text,
			variable=self.enable_hotkeys_var,
			style="Dark.TCheckbutton",
			command=self._on_hotkeys_toggle,
		)
		self.hotkeys_check.grid(row=0, column=0, sticky="w")
		if keyboard is None:
			self.hotkeys_check.state(["disabled"])  # keyboard module not available

		# Status
		status = ttk.Label(container, textvariable=self.status_var, style="Dark.TLabel")
		status.grid(row=4, column=0, columnspan=2, pady=(12, 0), sticky="w")

		for i in range(2):
			container.columnconfigure(i, weight=0)

	def start_clicking(self) -> None:
		if self.is_running:
			return
		try:
			delay_value = float(self.delay_var.get().strip())
			if delay_value <= 0:
				raise ValueError
		except ValueError:
			messagebox.showerror("Invalid Delay", "Please enter a positive number for delay (e.g. 0.1)")
			return

		self.is_running = True
		self.stop_event.clear()
		self._set_controls_state(running=True)
		self.status_var.set("Clicking… Press Stop to halt")

		self.worker_thread = threading.Thread(target=self._click_worker, args=(delay_value,), daemon=True)
		self.worker_thread.start()

	def stop_clicking(self) -> None:
		if not self.is_running:
			return
		self.stop_event.set()
		if self.worker_thread and self.worker_thread.is_alive():
			self.worker_thread.join(timeout=1.0)
		self.is_running = False
		self._set_controls_state(running=False)
		self.status_var.set("Stopped")

	def _toggle_clicking(self) -> None:
		# Schedule on Tk thread
		if self.is_running:
			self.root.after(0, self.stop_clicking)
		else:
			self.root.after(0, self.start_clicking)

	def _click_worker(self, delay_value: float) -> None:
		button_choice = self.button_var.get()
		while not self.stop_event.is_set():
			pyautogui.click(button=button_choice)
			time.sleep(delay_value)

	def _set_controls_state(self, running: bool) -> None:
		if running:
			self.start_btn.configure(state=tk.DISABLED)
			self.stop_btn.configure(state=tk.NORMAL)
		else:
			self.start_btn.configure(state=tk.NORMAL)
			self.stop_btn.configure(state=tk.DISABLED)

	def _on_hotkeys_toggle(self) -> None:
		if not keyboard:
			return
		if self.enable_hotkeys_var.get():
			self._register_hotkeys()
		else:
			self._unregister_hotkeys()

	def _maybe_register_hotkeys(self) -> None:
		if keyboard and self.enable_hotkeys_var.get():
			self._register_hotkeys()

	def _register_hotkeys(self) -> None:
		self._unregister_hotkeys()
		if not keyboard:
			return
		try:
			# Use F6 as a global toggle
			h = keyboard.add_hotkey("f6", self._toggle_clicking)
			self._hotkey_handles.append(h)
			self.status_var.set("Idle — Hotkey: F6 to Start/Stop")
		except Exception:
			pass

	def _unregister_hotkeys(self) -> None:
		if not keyboard:
			return
		try:
			keyboard.unhook_all_hotkeys()
			self._hotkey_handles.clear()
		except Exception:
			pass

	def _on_close(self) -> None:
		if self.is_running:
			if not messagebox.askyesno("Quit", "AutoClicker is running. Stop and exit?"):
				return
			self.stop_clicking()
		self._unregister_hotkeys()
		self.root.destroy()

	def _enable_win_dark_titlebar(self) -> None:
		"""Enable dark title bar on Windows 10 1809+ using DwmSetWindowAttribute.
		Silently no-ops on unsupported platforms/versions."""
		try:
			if sys.platform != "win32":
				return
			HWND = ctypes.windll.user32.GetParent(self.root.winfo_id())
			DWMWA_USE_IMMERSIVE_DARK_MODE = 20  # Windows 10 1903+
			DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_1903 = 19
			set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
			def _set(attr: int) -> int:
				value = ctypes.c_int(1)
				return set_window_attribute(HWND, ctypes.c_uint(attr), ctypes.byref(value), ctypes.sizeof(value))
			res = _set(DWMWA_USE_IMMERSIVE_DARK_MODE)
			if res != 0:
				_set(DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_1903)
		except Exception:
			pass


def main() -> None:
	root = tk.Tk()
	# Locate icon file when running as script or as PyInstaller bundle
	try:
		base_path = sys._MEIPASS  # type: ignore[attr-defined]
	except Exception:
		base_path = os.path.dirname(os.path.abspath(__file__))
	# Try both root and icon/ subfolder for icons (ico and png)
	candidate_icos = [
		os.path.join(base_path, "acbl.ico"),
		os.path.join(base_path, "icon", "acbl.ico"),
	]
	candidate_pngs = [
		os.path.join(base_path, "acbl.png"),
		os.path.join(base_path, "icon", "acbl.png"),
	]
	icon_ico = next((p for p in candidate_icos if os.path.exists(p)), None)
	icon_png = next((p for p in candidate_pngs if os.path.exists(p)), None)
	# Set bitmap icon (title bar on Windows)
	if icon_ico:
		try:
			root.iconbitmap(icon_ico)
		except Exception:
			pass
	# Also set iconphoto with PNG to influence taskbar in some environments
	if icon_png:
		try:
			photo = tk.PhotoImage(file=icon_png)
			root.iconphoto(True, photo)
		except Exception:
			pass
	app = AutoClickerApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()
