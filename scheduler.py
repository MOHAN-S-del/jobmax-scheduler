"""
scheduler.py — Greedy Job Scheduling Algorithm
================================================
Project : JobMax — Greedy Job Scheduler
Author  : (Your Name)
Subject : Design and Analysis of Algorithms

Algorithm : Greedy Job Sequencing with Deadlines
Time Complexity  : O(n log n)  — due to sorting
Space Complexity : O(n)        — for the slots array
"""


def schedule_jobs(jobs):
    """
    Greedy Job Scheduling Algorithm.

    Parameters:
        jobs (list of dict): Each job has:
            - 'id'       : unique job identifier
            - 'name'     : job name (e.g. "Fix Pipe")
            - 'deadline' : latest time unit by which job must finish
            - 'profit'   : profit earned if job is completed

    Returns:
        dict: {
            'scheduled'    : list of scheduled jobs with assigned slot,
            'skipped'      : list of jobs that could not be scheduled,
            'total_profit' : total profit earned,
            'slots'        : final slot assignments,
            'steps'        : step-by-step trace of algorithm decisions
        }
    """

    if not jobs:
        return {
            'scheduled': [],
            'skipped': [],
            'total_profit': 0,
            'slots': [],
            'steps': []
        }

    # ── STEP 1: Sort jobs by profit in descending order (Greedy Choice) ──
    # Greedy strategy: always consider the highest profit job first
    sorted_jobs = sorted(jobs, key=lambda j: j['profit'], reverse=True)

    # ── STEP 2: Find maximum deadline to determine number of time slots ──
    max_deadline = max(job['deadline'] for job in jobs)

    # ── STEP 3: Initialize all time slots as empty (None) ──
    # slots[0] represents time unit 1, slots[1] represents time unit 2, etc.
    slots = [None] * max_deadline

    scheduled = []
    skipped = []
    steps = []

    steps.append({
        'type': 'info',
        'message': f"Sorted {len(sorted_jobs)} jobs by profit (descending): "
                   + ", ".join(f"{j['name']} (₹{j['profit']})" for j in sorted_jobs)
    })

    # ── STEP 4: For each job (in order of decreasing profit) ──
    for job in sorted_jobs:

        # Find the latest available slot before or at the job's deadline
        # We go right-to-left to preserve earlier slots for future jobs
        placed = False
        for t in range(min(job['deadline'], max_deadline) - 1, -1, -1):
            if slots[t] is None:
                # ── GREEDY PLACEMENT: assign job to this slot ──
                slots[t] = job
                scheduled.append({**job, 'slot': t + 1})
                steps.append({
                    'type': 'scheduled',
                    'message': f"✓ '{job['name']}' (profit ₹{job['profit']}, deadline T{job['deadline']}) "
                               f"→ placed at slot {t + 1}"
                })
                placed = True
                break

        if not placed:
            # No available slot found before this job's deadline — skip it
            skipped.append(job)
            steps.append({
                'type': 'skipped',
                'message': f"✗ '{job['name']}' (profit ₹{job['profit']}, deadline T{job['deadline']}) "
                           f"— no available slot before deadline"
            })

    # ── STEP 5: Calculate total profit ──
    total_profit = sum(job['profit'] for job in scheduled)

    steps.append({
        'type': 'result',
        'message': f"Total profit = ₹{total_profit} | "
                   f"Jobs scheduled: {len(scheduled)} | "
                   f"Jobs skipped: {len(skipped)}"
    })

    return {
        'scheduled': scheduled,
        'skipped': skipped,
        'total_profit': total_profit,
        'slots': slots,
        'steps': steps
    }


def print_result(result):
    """Pretty-print the scheduling result to console."""
    print("\n" + "=" * 55)
    print("         JOBMAX — GREEDY SCHEDULER RESULT")
    print("=" * 55)

    print(f"\n{'Total Profit':.<30} ₹{result['total_profit']}")
    print(f"{'Jobs Scheduled':.<30} {len(result['scheduled'])}")
    print(f"{'Jobs Skipped':.<30} {len(result['skipped'])}")

    print("\n── Algorithm Steps ──")
    for step in result['steps']:
        print(f"  {step['message']}")

    print("\n── Timeline ──")
    for i, job in enumerate(result['slots']):
        slot_label = f"  Slot T{i+1}"
        if job:
            print(f"{slot_label:.<20} {job['name']} (₹{job['profit']})")
        else:
            print(f"{slot_label:.<20} [idle]")

    if result['skipped']:
        print("\n── Skipped Jobs ──")
        for job in result['skipped']:
            print(f"  ✗ {job['name']} (₹{job['profit']}, deadline T{job['deadline']})")

    print("\n" + "=" * 55)


# ── Test / Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    sample_jobs = [
        {'id': 1, 'name': 'Fix Water Pipe',  'deadline': 2, 'profit': 500},
        {'id': 2, 'name': 'Build Cabinet',   'deadline': 1, 'profit': 300},
        {'id': 3, 'name': 'Paint Wall',      'deadline': 3, 'profit': 400},
        {'id': 4, 'name': 'Lay Foundation',  'deadline': 2, 'profit': 700},
        {'id': 5, 'name': 'Wire Circuit',    'deadline': 3, 'profit': 600},
        {'id': 6, 'name': 'Install Sink',    'deadline': 1, 'profit': 200},
        {'id': 7, 'name': 'Floor Tiles',     'deadline': 4, 'profit': 350},
    ]

    print("\nInput Jobs:")
    print(f"  {'#':<4} {'Name':<20} {'Deadline':<12} {'Profit'}")
    print("  " + "-" * 45)
    for i, j in enumerate(sample_jobs, 1):
        print(f"  {i:<4} {j['name']:<20} T{j['deadline']:<11} ₹{j['profit']}")

    result = schedule_jobs(sample_jobs)
    print_result(result)
