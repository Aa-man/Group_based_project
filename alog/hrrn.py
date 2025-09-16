
def run(processes):
    import copy
    result_table = []
    schedule = []

    procs = copy.deepcopy(processes)
    time = 0
    completed = set()

    while len(completed) < len(procs):
        ready = [p for p in procs if p['arrival'] <= time and p['pid'] not in completed]
        if not ready:
            time += 1
            continue

        for p in ready:
            waiting_time = time - p['arrival']
            response_ratio = (waiting_time + p['burst']) / p['burst']
            p['rr'] = response_ratio

        current = max(ready, key=lambda x: x['rr'])
        pid = current['pid']
        start = max(time, current['arrival'])
        end = start + current['burst']
        time = end

        completion = end
        tat = completion - current['arrival']
        wt = tat - current['burst']

        result_table.append({
            'pid': pid,
            'arrival': current['arrival'],
            'burst': current['burst'],
            'completion': completion,
            'turnaround': tat,
            'waiting': wt,
            'priority': current.get('priority', '-')
        })
        schedule.append((pid, start, end))
        completed.add(pid)

    print("\nPID\tAT\tBT\tCT\tTAT\tWT\tPR")
    for r in sorted(result_table, key=lambda x: x['pid']):
        print(f"{r['pid']}\t{r['arrival']}\t{r['burst']}\t{r['completion']}\t{r['turnaround']}\t{r['waiting']}\t{r['priority']}")

    from utils.gantt_chart import draw_gantt_chart
    draw_gantt_chart(schedule)
