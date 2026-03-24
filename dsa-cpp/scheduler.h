#ifndef SCHEDULER_H
#define SCHEDULER_H

#include <vector>
#include <string>
#include "job.h"

// ─────────────────────────────────────────────────────────────
//  scheduler.h — Greedy Job Scheduler declarations
//
//  Mirrors Python schedule_jobs() return dict exactly:
//  {
//    'scheduled'    : list of scheduled jobs with slot
//    'skipped'      : list of jobs that couldn't be scheduled
//    'total_profit' : total profit earned
//    'slots'        : final slot assignments (None = idle)
//    'steps'        : step-by-step trace messages
//  }
// ─────────────────────────────────────────────────────────────

// Step trace — mirrors Python steps list of dicts
// {'type': 'info'|'scheduled'|'skipped'|'result', 'message': "..."}
struct Step {
    std::string type;     // "info" | "scheduled" | "skipped" | "result"
    std::string message;  // human-readable trace message
};

// Result — mirrors Python schedule_jobs() return dict
struct ScheduleResult {
    std::vector<Job>    scheduled;      // → result['scheduled']
    std::vector<Job>    skipped;        // → result['skipped']
    int                 total_profit;   // → result['total_profit']
    std::vector<int>    slots;          // → result['slots']  (-1 = idle, else index into scheduled)
    std::vector<Step>   steps;          // → result['steps']
};

// ── Function declarations ─────────────────────────────────────

// Main algorithm — mirrors: def schedule_jobs(jobs)
ScheduleResult schedule_jobs(std::vector<Job> jobs);

// Pretty printer — mirrors: def print_result(result)
void print_result(const ScheduleResult& result);

#endif // SCHEDULER_H
