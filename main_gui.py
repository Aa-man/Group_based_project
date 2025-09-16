import tkinter as tk
from tkinter import messagebox, ttk
from utils.gantt_chart import draw_gantt_chart
import importlib

# Globals to store entries for processes
arrival_entries = []
burst_entries = []
priority_entries = []
queue_entries = []

def create_process_entries():
    try:
        # Clear previous widgets placed below row 1
        for widget in root.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()

        num_processes = int(num_processes_entry.get())
        arrival_entries.clear()
        burst_entries.clear()
        priority_entries.clear()
        queue_entries.clear()

        # Headers
        tk.Label(root, text="PID").grid(row=2, column=0)
        tk.Label(root, text="Arrival Time").grid(row=2, column=1)
        tk.Label(root, text="Burst Time").grid(row=2, column=2)
        tk.Label(root, text="Priority (opt)").grid(row=2, column=3)
        tk.Label(root, text="Queue (opt)").grid(row=2, column=4)

        for i in range(num_processes):
            tk.Label(root, text=f"P{i+1}").grid(row=i + 3, column=0)
            ae = tk.Entry(root)
            be = tk.Entry(root)
            pe = tk.Entry(root)
            qe = tk.Entry(root)

            ae.grid(row=i + 3, column=1)
            be.grid(row=i + 3, column=2)
            pe.grid(row=i + 3, column=3)
            qe.grid(row=i + 3, column=4)

            arrival_entries.append(ae)
            burst_entries.append(be)
            priority_entries.append(pe)
            queue_entries.append(qe)

        # Place algorithm selector and run button below the last entry row
        algorithm_label.grid(row=num_processes + 3, column=0, pady=10)
        algorithm_dropdown.grid(row=num_processes + 3, column=1)
        run_button.grid(row=num_processes + 4, column=0, columnspan=2, pady=10)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of processes.")

def validate_int(val):
    try:
        return int(val)
    except:
        return None

def run_algorithm():
    try:
        num_processes = int(num_processes_entry.get())
        processes = []

        for i in range(num_processes):
            pid = i + 1
            arrival = validate_int(arrival_entries[i].get())
            burst = validate_int(burst_entries[i].get())
            priority = validate_int(priority_entries[i].get())
            queue = validate_int(queue_entries[i].get())

            if arrival is None or burst is None:
                messagebox.showerror("Input Error", f"Arrival and Burst times are required for Process {pid}.")
                return
            
            process = {'pid': pid, 'arrival': arrival, 'burst': burst}
            if priority is not None:
                process['priority'] = priority
            if queue is not None:
                process['queue'] = queue
            processes.append(process)

        selected_algorithm = algorithm_var.get().lower()  # match your module names

        # Dynamically import and run selected algorithm
        try:
            module = importlib.import_module(f"algorithms.{selected_algorithm}")
            schedule = module.run(processes)
            draw_gantt_chart(schedule)
        except ModuleNotFoundError:
            messagebox.showerror("Error", f"Algorithm '{selected_algorithm}' not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error running algorithm: {e}")

    except Exception as e:
        messagebox.showerror("Runtime Error", f"An error occurred: {e}")

# Main window setup
root = tk.Tk()
root.title("CPU Scheduling Algorithms")
root.geometry("700x500")
root.resizable(False, False)

# Number of processes input
tk.Label(root, text="Enter number of processes:").grid(row=0, column=0, padx=5, pady=5)
num_processes_entry = tk.Entry(root)
num_processes_entry.grid(row=0, column=1, padx=5, pady=5)

create_button = tk.Button(root, text="Create Process Entries", command=create_process_entries)
create_button.grid(row=0, column=2, padx=5, pady=5)

# Algorithm dropdown
algorithm_label = tk.Label(root, text="Select Algorithm:")
algorithm_var = tk.StringVar()
algorithm_dropdown = ttk.Combobox(root, textvariable=algorithm_var, state="readonly")
algorithm_dropdown['values'] = [
    "fcfs", "hrrn", "mlq", "priority_np",
    "priority_p", "round_robin", "sjf_np", "srtf"
]
algorithm_dropdown.set("fcfs")

# Run button
run_button = tk.Button(root, text="Run Algorithm", command=run_algorithm)

root.mainloop()