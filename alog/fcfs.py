
def run(processes):
    result_table = []
    schedule = []

    time = 0
    for p in sorted(processes, key=lambda x: x['arrival']):
        start = max(time, p['arrival'])
        end = start + p['burst']
        time = end

        completion = end
        turnaround = completion - p['arrival']
        waiting = turnaround - p['burst']

        result_table.append({
            'pid': p['pid'],
            'arrival': p['arrival'],
            'burst': p['burst'],
            'completion': completion,
            'turnaround': turnaround,
            'waiting': waiting,
            'priority': p.get('priority', '-')
        })

        schedule.append((p['pid'], start, end))

    print("\nPID\tAT\tBT\tCT\tTAT\tWT\tPR")
    for r in result_table:
        print(f"{r['pid']}\t{r['arrival']}\t{r['burst']}\t{r['completion']}\t{r['turnaround']}\t{r['waiting']}\t{r['priority']}")

    from utils.gantt_chart import draw_gantt_chart
    draw_gantt_chart(schedule)
