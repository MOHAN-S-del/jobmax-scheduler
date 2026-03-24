/*
 * scheduler.cpp — Greedy Job Scheduling Algorithm
 * ================================================
 * Project   : JobMax — Greedy Job Scheduler
 * Subject   : Design and Analysis of Algorithms
 * Algorithm : Greedy Job Sequencing with Deadlines
 *
 * Time Complexity  : O(n log n) — due to sorting
 * Space Complexity : O(n)       — for the slots array
 *
 * NOTE: Variable names match Python scheduler.py exactly:
 *   sorted_jobs, max_deadline, slots, scheduled,
 *   skipped, steps, total_profit, placed
 */

#include "scheduler.h"
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <sstream>

// ─────────────────────────────────────────────────────────────
//  schedule_jobs()
//  Mirrors Python: def schedule_jobs(jobs)
// ─────────────────────────────────────────────────────────────
ScheduleResult schedule_jobs(std::vector<Job> jobs) {

    ScheduleResult result;
    result.total_profit = 0;

    // Handle empty input — mirrors Python: if not jobs
    if (jobs.empty()) {
        return result;
    }

    // ── STEP 1: Sort jobs by profit descending (Greedy Choice) ──
    // Mirrors Python: sorted_jobs = sorted(jobs, key=lambda j: j['profit'], reverse=True)
    std::vector<Job> sorted_jobs = jobs;
    std::sort(sorted_jobs.begin(), sorted_jobs.end(),
        [](const Job& a, const Job& b) {
            return a.profit > b.profit;
        });

    // ── STEP 2: Find maximum deadline ──
    // Mirrors Python: max_deadline = max(job['deadline'] for job in jobs)
    int max_deadline = 0;
    for (const Job& job : jobs) {
        if (job.deadline > max_deadline)
            max_deadline = job.deadline;
    }

    // ── STEP 3: Initialize slots as empty (-1 = None in Python) ──
    // Mirrors Python: slots = [None] * max_deadline
    std::vector<int> slots(max_deadline, -1);  // -1 means idle

    // Vectors to hold scheduled and skipped jobs
    // Mirrors Python: scheduled = []  skipped = []  steps = []
    std::vector<Job>  scheduled;
    std::vector<Job>  skipped;
    std::vector<Step> steps;

    // Build sorted names for info step
    std::string sorted_names = "";
    for (size_t i = 0; i < sorted_jobs.size(); i++) {
        sorted_names += sorted_jobs[i].name + " (Rs." + std::to_string(sorted_jobs[i].profit) + ")";
        if (i < sorted_jobs.size() - 1) sorted_names += ", ";
    }
    steps.push_back({
        "info",
        "Sorted " + std::to_string(sorted_jobs.size()) +
        " jobs by profit (descending): " + sorted_names
    });

    // ── STEP 4: For each job in sorted order ──
    // Mirrors Python: for job in sorted_jobs
    for (Job& job : sorted_jobs) {

        // Find latest available slot before or at deadline
        // Mirrors Python: for t in range(min(job['deadline'], max_deadline) - 1, -1, -1)
        bool placed = false;
        int  limit  = std::min(job.deadline, max_deadline);

        for (int t = limit - 1; t >= 0; t--) {
            if (slots[t] == -1) {

                // ── GREEDY PLACEMENT ──
                job.slot  = t + 1;
                scheduled.push_back(job);
                slots[t]  = (int)scheduled.size() - 1;  // store index

                steps.push_back({
                    "scheduled",
                    "✓ '" + job.name +
                    "' (profit Rs." + std::to_string(job.profit) +
                    ", deadline T" + std::to_string(job.deadline) + ")" +
                    " → placed at slot " + std::to_string(t + 1)
                });

                placed = true;
                break;
            }
        }

        // Mirrors Python: if not placed → skipped.append(job)
        if (!placed) {
            skipped.push_back(job);
            steps.push_back({
                "skipped",
                "✗ '" + job.name +
                "' (profit Rs." + std::to_string(job.profit) +
                ", deadline T" + std::to_string(job.deadline) + ")" +
                " — no available slot before deadline"
            });
        }
    }

    // ── STEP 5: Calculate total profit ──
    // Mirrors Python: total_profit = sum(job['profit'] for job in scheduled)
    int total_profit = 0;
    for (const Job& job : scheduled) {
        total_profit += job.profit;
    }

    steps.push_back({
        "result",
        "Total profit = Rs." + std::to_string(total_profit) +
        " | Jobs scheduled: " + std::to_string(scheduled.size()) +
        " | Jobs skipped: "   + std::to_string(skipped.size())
    });

    // Fill result struct — mirrors Python return dict
    result.scheduled     = scheduled;
    result.skipped       = skipped;
    result.total_profit  = total_profit;
    result.slots         = slots;
    result.steps         = steps;

    return result;
}

// ─────────────────────────────────────────────────────────────
//  print_result()
//  Mirrors Python: def print_result(result)
// ─────────────────────────────────────────────────────────────
void print_result(const ScheduleResult& result) {
    std::cout << "\n" << std::string(55, '=') << "\n";
    std::cout << " JOBMAX — GREEDY SCHEDULER RESULT\n";
    std::cout << std::string(55, '=') << "\n";

    std::cout << "\n" << std::left << std::setw(30) << "Total Profit"
              << " Rs." << result.total_profit << "\n";
    std::cout << std::setw(30) << "Jobs Scheduled"
              << " "    << result.scheduled.size() << "\n";
    std::cout << std::setw(30) << "Jobs Skipped"
              << " "    << result.skipped.size()   << "\n";

    // Algorithm steps trace
    std::cout << "\n── Algorithm Steps ──\n";
    for (const Step& step : result.steps) {
        std::cout << "  " << step.message << "\n";
    }

    // Timeline — mirrors Python slots loop
    std::cout << "\n── Timeline ──\n";
    for (size_t i = 0; i < result.slots.size(); i++) {
        std::string label = " Slot T" + std::to_string(i + 1);
        if (result.slots[i] != -1) {
            const Job& j = result.scheduled[result.slots[i]];
            std::cout << std::left << std::setw(20) << label
                      << j.name << " (Rs." << j.profit << ")\n";
        } else {
            std::cout << std::left << std::setw(20) << label << "[idle]\n";
        }
    }

    // Skipped jobs
    if (!result.skipped.empty()) {
        std::cout << "\n── Skipped Jobs ──\n";
        for (const Job& job : result.skipped) {
            std::cout << "  ✗ " << job.name
                      << " (Rs." << job.profit
                      << ", deadline T" << job.deadline << ")\n";
        }
    }

    std::cout << "\n" << std::string(55, '=') << "\n";
}
