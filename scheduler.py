"""
scheduler.py — Greedy Job Scheduling Algorithm for Freelancers
================================================================
Project : FreelanceMax — Smart Project Scheduler
Author  : (Your Name)
Subject : Design and Analysis of Algorithms

Algorithm : Greedy Project Sequencing with Deadlines
Time Complexity  : O(n log n)  — due to sorting
Space Complexity : O(n)        — for the slots array
"""


def schedule_jobs(jobs):
    """
    Greedy Project Scheduling Algorithm for Freelancers.

    Parameters:
        jobs (list of dict): Each project has:
            - 'id'       : unique project identifier
            - 'job_type' : project type (Web Development, Design, etc.)
            - 'name'     : project name (e.g. "E-commerce Website")
            - 'deadline' : datetime string (ISO format)
            - 'profit'   : budget/earnings for the project

    Returns:
        dict: {
            'scheduled'    : list of scheduled projects with assigned slot,
            'skipped'      : list of projects that could not be scheduled,
            'total_profit' : total earnings,
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

    # ── STEP 1: Sort projects by profit in descending order (Greedy Choice) ──
    # Greedy strategy: always consider the highest budget project first
    sorted_jobs = sorted(jobs, key=lambda j: j['profit'], reverse=True)

    # ── STEP 2: Convert deadlines to days from now ──
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    
    # Calculate days until deadline for each project
    for job in sorted_jobs:
        try:
            deadline_dt = datetime.fromisoformat(job['deadline'].replace('Z', '+00:00'))
            days_until_deadline = (deadline_dt - now).days + 1  # +1 to make it 1-based
            job['_days_deadline'] = max(1, days_until_deadline)  # Ensure at least 1 day
        except:
            job['_days_deadline'] = 7  # Default to 7 days if parsing fails

    # Find maximum deadline in days
    max_deadline = max(job['_days_deadline'] for job in sorted_jobs)

    # ── STEP 3: Initialize all time slots as empty (None) ──
    # slots[0] represents day 1, slots[1] represents day 2, etc.
    slots = [None] * max_deadline

    scheduled = []
    skipped = []
    steps = []

    steps.append({
        'type': 'info',
        'message': f"Sorted {len(sorted_jobs)} projects by budget (descending): "
                   + ", ".join(f"{j['name']} (₹{j['profit']})" for j in sorted_jobs)
    })

    # ── STEP 4: For each project (in order of decreasing profit) ──
    for job in sorted_jobs:

        # Find the latest available slot before or at the project's deadline
        # We go right-to-left to preserve earlier slots for future projects
        placed = False
        days_deadline = job['_days_deadline']
        
        for t in range(min(days_deadline, max_deadline) - 1, -1, -1):
            if slots[t] is None:
                # ── GREEDY PLACEMENT: assign project to this slot ──
                slots[t] = job
                scheduled.append({**job, 'slot': t + 1, 'slot_date': f"Day {t + 1}"})
                steps.append({
                    'type': 'scheduled',
                    'message': f"✓ '{job['name']}' ({job['job_type']}, budget ₹{job['profit']}, deadline {days_deadline} days) "
                               f"→ scheduled for Day {t + 1}"
                })
                placed = True
                break

        if not placed:
            # No available slot found before this project's deadline — skip it
            skipped.append(job)
            steps.append({
                'type': 'skipped',
                'message': f"✗ '{job['name']}' ({job['job_type']}, budget ₹{job['profit']}, deadline {days_deadline} days) "
                           f"— no available slot before deadline"
            })

    # ── STEP 5: Calculate total earnings ──
    total_profit = sum(job['profit'] for job in scheduled)

    steps.append({
        'type': 'result',
        'message': f"Total earnings = ₹{total_profit} | "
                   f"Projects scheduled: {len(scheduled)} | "
                   f"Projects skipped: {len(skipped)}"
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
