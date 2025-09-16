
import importlib
import sys
from utils.gantt_chart import draw_gantt_chart

print("Welcome to PyOS v1.0")
print("Type 'help' to list commands.")

available_algorithms = [
    "fcfs", "hrrn", "mlq", "priority_np",
    "priority_p", "round_robin", "sjf_np", "srtf"
]

last_schedule = []

def load_algorithm(algo_name, processes):
    try:
        module = importlib.import_module(f"algorithms.{algo_name}")
        global last_schedule
        last_schedule = module.run(processes)
    except ModuleNotFoundError:
        print("Algorithm not found.")
    except Exception as e:
        print("Error running algorithm:", e)

def get_process_input():
    processes = []
    n = int(input("Enter number of processes: "))
    for i in range(n):
        print(f"\nProcess {i+1}")
        pid = int(input("PID: "))
        arrival = int(input("Arrival Time: "))
        burst = int(input("Burst Time: "))
        priority = input("Priority (optional): ")
        queue = input("Queue (for MLQ/MLFQ only, optional): ")

        process = {'pid': pid, 'arrival': arrival, 'burst': burst}
        if priority:
            process['priority'] = int(priority)
        if queue:
            process['queue'] = int(queue)
        processes.append(process)
    return processes

while True:
    cmd = input("PyOS> ").strip().lower()

    if cmd == "help":
        print("Commands:")
        print(" run [algorithm]  - Run a scheduling algorithm")
        print(" show_gantt       - Show Gantt chart of last run")
        print(" exit             - Exit the OS")
        print("\nAvailable Algorithms:")
        for algo in available_algorithms:
            print(f" - {algo}")

    elif cmd == "list_algos":
        print("Available Algorithms:")
        for algo in available_algorithms:
            print(" -", algo)

    elif cmd.startswith("run "):
        algo = cmd.split(" ")[1]
        if algo not in available_algorithms:
            print("Invalid algorithm. Use 'list_algos' to see options.")
        else:
            processes = get_process_input()
            load_algorithm(algo, processes)

    elif cmd == "show_gantt":
        if last_schedule:
            draw_gantt_chart(last_schedule)
        else:
            print("Run an algorithm first.")

    elif cmd == "exit":
        print("Shutting down PyOS.")
        sys.exit()

    else:
        print("Unknown command. Type 'help'.")
