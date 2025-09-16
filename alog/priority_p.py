
def run(processes):
    import copy
    result_table = []
    schedule = []

    procs = copy.deepcopy(processes)
    time = 0
    remaining = {p['pid']: p['burst'] for p in procs}
    complete = 0
    n = len(procs)
    last_pid = None
    start_time = {}

    while complete < n:
        ready = [p for p in procs if p['arrival'] <= time and remaining[p['pid']] > 0]
        if not ready:
            time += 1
            continue

        current = min(ready, key=lambda x: x['priority'])
        pid = current['pid']

        if pid != last_pid:
            if last_pid is not None and remaining[last_pid] > 0:
                schedule[-1] = (schedule[-1][0], schedule[-1][1], time)
            schedule.append((pid, time, time + 1))
        else:
            schedule[-1] = (pid, schedule[-1][1], time + 1)

        if pid not in start_time:
            start_time[pid] = time

        remaining[pid] -= 1
        time += 1

        if remaining[pid] == 0:
            complete += 1
            finish_time = time
            tat = finish_time - current['arrival']
            wt = tat - current['burst']
            result_table.append({
                'pid': pid,
                'arrival': current['arrival'],
                'burst': current['burst'],
                'completion': finish_time,
                'turnaround': tat,
                'waiting': wt,
                'priority': current['priority']
            })

        last_pid = pid

    print("\nPID\tAT\tBT\tCT\tTAT\tWT\tPR")
    for r in sorted(result_table, key=lambda x: x['pid']):
        print(f"{r['pid']}\t{r['arrival']}\t{r['burst']}\t{r['completion']}\t{r['turnaround']}\t{r['waiting']}\t{r['priority']}")

    from utils.gantt_chart import draw_gantt_chart
    draw_gantt_chart(schedule)
