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
            'steps': []
        }

    # Sort jobs by profit (descending)
    sorted_jobs = sorted(jobs, key=lambda j: j['profit'], reverse=True)
    
    # Find max deadline
    max_deadline = max(job['deadline'] for job in jobs)
    
    # Initialize slots
    slots = [None] * max_deadline
    scheduled = []
    skipped = []
    
    # Greedy placement
    for job in sorted_jobs:
        placed = False
        for t in range(min(job['deadline'], max_deadline) - 1, -1, -1):
            if slots[t] is None:
                slots[t] = job
                scheduled.append({**job, 'slot': t + 1})
                placed = True
                break
        
        if not placed:
            skipped.append(job)
    
    total_profit = sum(job['profit'] for job in scheduled)
    
    return {
        'scheduled': scheduled,
        'skipped': skipped,
        'total_profit': total_profit,
        'slots': slots,
        'steps': []
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
