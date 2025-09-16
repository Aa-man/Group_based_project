def run(processes):
    from utils.gantt_chart import draw_gantt_chart

    queue1 = [p.copy() for p in processes if p['queue'] == 1]
    queue2 = [p.copy() for p in processes if p['queue'] == 2]

    time = 0
    schedule = []
    completed = set()

    # Sort by arrival time initially
    queue1.sort(key=lambda x: x['arrival'])
    queue2.sort(key=lambda x: x['arrival'])

    ready_q1 = []
    ready_q2 = []

    time_quantum = 2

    while len(completed) < len(processes):
        # Add newly arrived processes
        for p in queue1:
            if p['arrival'] <= time and p['pid'] not in completed and p not in ready_q1:
                ready_q1.append(p)
        for p in queue2:
            if p['arrival'] <= time and p['pid'] not in completed and p not in ready_q2:
                ready_q2.append(p)

        if ready_q1:
            p = ready_q1.pop(0)
            exec_time = min(time_quantum, p['burst'])
            start = time
            end = time + exec_time
            schedule.append((p['pid'], start, end))
            p['burst'] -= exec_time
            time += exec_time
            if p['burst'] > 0:
                ready_q1.append(p)
            else:
                completed.add(p['pid'])
        elif ready_q2:
            p = ready_q2.pop(0)
            start = time
            end = time + p['burst']
            schedule.append((p['pid'], start, end))
            time = end
            completed.add(p['pid'])
        else:
            time += 1  # Idle

    print("MLQ Scheduling Complete.\nGantt Chart:")
    draw_gantt_chart(schedule)
