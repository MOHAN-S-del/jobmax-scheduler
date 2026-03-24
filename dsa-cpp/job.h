#ifndef JOB_H
#define JOB_H

#include <string>

// ─────────────────────────────────────────────────────────────
//  job.h — Job data structure
//  Matches Python dict keys exactly:
//  {'id', 'name', 'deadline', 'profit', 'slot'}
// ─────────────────────────────────────────────────────────────

struct Job {
    int         id;          // unique job identifier       → j['id']
    std::string name;        // job name e.g. "Fix Pipe"   → j['name']
    int         deadline;    // latest time slot allowed    → j['deadline']
    int         profit;      // profit if completed         → j['profit']
    int         slot;        // assigned slot (0 = not set) → j['slot']

    // Constructor — slot defaults to 0 (unassigned)
    Job(int id, std::string name, int deadline, int profit, int slot = 0)
        : id(id), name(name), deadline(deadline), profit(profit), slot(slot) {}
};

#endif // JOB_H
