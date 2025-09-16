
import tkinter as tk
import subprocess
import sys
import os

def launch_gui():
    print("Launching GUI...")
    try:
        subprocess.run([sys.executable, "main_gui.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to launch GUI:", e)

def launch_cli():
    print("Launching CLI...")
    try:
        subprocess.run([sys.executable, "main_cli.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to launch CLI:", e)

def launch_menu():
    root = tk.Tk()
    root.title("PyOS Launcher")
    root.geometry("300x180")

    label = tk.Label(root, text="Welcome to PyOS", font=("Arial", 14))
    label.pack(pady=20)

    btn_cli = tk.Button(root, text="Launch CLI Mode", command=lambda: [root.destroy(), launch_cli()])
    btn_cli.pack(pady=10)

    btn_gui = tk.Button(root, text="Launch GUI Mode", command=lambda: [root.destroy(), launch_gui()])
    btn_gui.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    print("PyOS Launcher started.")
    if not os.path.exists("main_gui.py") or not os.path.exists("main_cli.py"):
        print("Error: main_gui.py or main_cli.py not found in this directory.")
    else:
        launch_menu()
