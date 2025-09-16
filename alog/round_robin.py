
def run(processes, time_quantum=2):
    from collections import deque
    import copy
    result_table = []
    schedule = []

    procs = sorted(copy.deepcopy(processes), key=lambda x: x['arrival'])
    n = len(procs)
    queue = deque()
    time = 0
    remaining = {p['pid']: p['burst'] for p in procs}
    completed = {}
    i = 0

    while len(completed) < n:
        while i < n and procs[i]['arrival'] <= time:
            queue.append(procs[i])
            i += 1

        if not queue:
            time += 1
            continue

        current = queue.popleft()
        pid = current['pid']
        start = time
        execute_time = min(time_quantum, remaining[pid])
        time += execute_time
        remaining[pid] -= execute_time
        schedule.append((pid, start, time))

        while i < n and procs[i]['arrival'] <= time:
            queue.append(procs[i])
            i += 1

        if remaining[pid] > 0:
            queue.append(current)
        else:
            completion = time
            turnaround = completion - current['arrival']
            waiting = turnaround - current['burst']
            result_table.append({
                'pid': pid,
                'arrival': current['arrival'],
                'burst': current['burst'],
                'completion': completion,
                'turnaround': turnaround,
                'waiting': waiting,
                'priority': current.get('priority', '-')
            })
            completed[pid] = True

    print("\nPID\tAT\tBT\tCT\tTAT\tWT\tPR")
    for r in sorted(result_table, key=lambda x: x['pid']):
        print(f"{r['pid']}\t{r['arrival']}\t{r['burst']}\t{r['completion']}\t{r['turnaround']}\t{r['waiting']}\t{r['priority']}")

    from utils.gantt_chart import draw_gantt_chart
    draw_gantt_chart(schedule)
