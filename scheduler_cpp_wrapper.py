"""
scheduler_cpp_wrapper.py
========================
Wrapper to call C++ greedy scheduler executable
Falls back to pure Python if C++ executable not found
"""

import subprocess
import json
import os
import platform
from pathlib import Path
from datetime import datetime, date

def calculate_days_until_deadline(deadline_str):
    """Calculate days until deadline from ISO string or integer"""
    if isinstance(deadline_str, int):
        return max(0, deadline_str)
    
    try:
        # Parse ISO datetime string (e.g., "2024-01-15T10:00:00")
        deadline_dt = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
        now = datetime.now(deadline_dt.tzinfo)
        
        # Get beginning of today for fair comparison
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if deadline_dt < today_start:
            return -2 # Past deadline
            
        diff = deadline_dt - now
        days_diff = diff.days
        
        return max(0, days_diff + 1)
    except (ValueError, TypeError):
        return 0

def get_scheduler_path():
    """Get path to compiled C++ scheduler executable"""
    project_dir = Path(__file__).parent
    
    if platform.system() == "Windows":
        executable = project_dir / "build" / "Debug" / "scheduler.exe"
    else:
        executable = project_dir / "build" / "scheduler"
    
    return executable if executable.exists() else None


def schedule_jobs_cpp(jobs):
    """
    Run greedy algorithm using C++ executable
    
    Parameters:
        jobs (list of dict): Each job has 'id', 'name', 'deadline', 'profit'
    
    Returns:
        dict: Scheduling result
    """
    scheduler_exe = get_scheduler_path()
    
    if not scheduler_exe:
        raise FileNotFoundError(
            "C++ scheduler executable not found. "
            "Please run: bash build.sh"
        )
    
    # Convert jobs to JSON string
    jobs_json = json.dumps(jobs)
    
    try:
        # Call C++ executable with JSON via stdin
        result = subprocess.run(
            [str(scheduler_exe)],
            input=jobs_json,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"C++ scheduler error: {result.stderr}")
        
        # Parse output JSON
        output = json.loads(result.stdout)
        
        # Return full output including steps
        return {
            'scheduled': output.get('scheduled', []),
            'skipped': output.get('skipped', []),
            'total_profit': output.get('total_profit', 0),
            'slots': [],  # Not needed in this format
            'steps': output.get('steps', [])  # Include steps from C++ scheduler
        }
    
    except subprocess.TimeoutExpired:
        raise RuntimeError("C++ Scheduler timeout")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse C++ output: {e}")


def schedule_jobs_python(jobs):
    """
    Fallback: Pure Python implementation of greedy algorithm
    Used if C++ executable not available
    """
    if not jobs:
        return {
            'scheduled': [],
            'skipped': [],
            'total_profit': 0,
            'slots': [],
            'steps': ["No jobs to schedule"]
        }

    # Pre-process jobs to calculate day deadlines
    processed_jobs = []
    for job in jobs:
        processed_job = job.copy()
        processed_job['days_deadline'] = calculate_days_until_deadline(job.get('deadline', 0))
        processed_jobs.append(processed_job)

    # Sort jobs by profit (descending)
    sorted_jobs = sorted(processed_jobs, key=lambda j: j['profit'], reverse=True)
    
    # Find max deadline
    valid_deadlines = [job['days_deadline'] for job in sorted_jobs if job['days_deadline'] > 0]
    max_deadline = max(valid_deadlines) if valid_deadlines else 0
    
    # Initialize slots
    slots = [None] * max_deadline
    scheduled = []
    skipped = []
    steps = [f"Step 1: Sorting {len(jobs)} jobs by profit (descending)"]
    steps.append(f"Step 2: Maximum deadline is {max_deadline} days")
    steps.append(f"Step 3: Initialized {max_deadline} time slots")
    steps.append("Step 4: Scheduling jobs in profit order")
    
    # Greedy placement
    for job in sorted_jobs:
        if job['days_deadline'] == -2:
            skipped.append(job)
            steps.append(f"  ✗ Skipped '{job['name']}' (₹{job['profit']}) - Deadline was in the past")
            continue

        placed = False
        limit = min(job['days_deadline'], max_deadline)
        for t in range(limit - 1, -1, -1):
            if slots[t] is None:
                slots[t] = job['name']
                scheduled.append({
                    'id': job.get('id'),
                    'name': job['name'],
                    'day': t + 1,
                    'profit': job['profit'],
                    'job_type': job.get('job_type', 'General')
                })
                placed = True
                steps.append(f"  ✓ Scheduled '{job['name']}' (₹{job['profit']}) on day {t + 1}")
                break
        
        if not placed:
            skipped.append(job)
            steps.append(f"  ✗ Skipped '{job['name']}' (₹{job['profit']}) - no available slot before deadline")
    
    total_profit = sum(job['profit'] for job in scheduled)
    steps.append(f"Step 5: Scheduling complete. Total profit: ₹{total_profit}")
    
    return {
        'scheduled': scheduled,
        'skipped': skipped,
        'total_profit': total_profit,
        'slots': [],  # Frontend expects 'scheduled' with 'day' info
        'steps': steps
    }


def schedule_jobs(jobs, use_cpp=True):
    """
    Schedule jobs using greedy algorithm
    
    Parameters:
        jobs (list of dict): Job data
        use_cpp (bool): Try to use C++ version first
    
    Returns:
        dict: Scheduling result
    """
    if use_cpp:
        try:
            return schedule_jobs_cpp(jobs)
        except Exception as e:
            print(f"⚠️  C++ scheduler failed: {e}. Falling back to Python...")
    
    return schedule_jobs_python(jobs)
