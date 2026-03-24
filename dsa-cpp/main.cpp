/*
 * main.cpp — JobMax Entry Point
 * ==============================
 * Mirrors Python:  if __name__ == "__main__":
 *
 * Uses the EXACT same sample_jobs as Python scheduler.py:
 *   Fix Water Pipe, Build Cabinet, Paint Wall,
 *   Lay Foundation, Wire Circuit, Install Sink, Floor Tiles
 */

#include <iostream>
#include <iomanip>
#include <vector>
#include "job.h"
#include "scheduler.h"

int main() {

    // ── Sample jobs — mirrors Python sample_jobs list exactly ──
    // {'id': 1, 'name': 'Fix Water Pipe', 'deadline': 2, 'profit': 500}
    std::vector<Job> sample_jobs = {
        Job(1, "Fix Water Pipe",  2, 500),
        Job(2, "Build Cabinet",   1, 300),
        Job(3, "Paint Wall",      3, 400),
        Job(4, "Lay Foundation",  2, 700),
        Job(5, "Wire Circuit",    3, 600),
        Job(6, "Install Sink",    1, 200),
        Job(7, "Floor Tiles",     4, 350),
    };

    // ── Print input table ──
    std::cout << "\nInput Jobs:\n";
    std::cout << "  " << std::left
              << std::setw(5)  << "#"
              << std::setw(22) << "Name"
              << std::setw(12) << "Deadline"
              << "Profit\n";
    std::cout << "  " << std::string(45, '-') << "\n";

    for (size_t i = 0; i < sample_jobs.size(); i++) {
        std::cout << "  "
                  << std::left  << std::setw(5)  << (i + 1)
                  << std::setw(22) << sample_jobs[i].name
                  << "T" << std::setw(11) << sample_jobs[i].deadline
                  << "Rs." << sample_jobs[i].profit << "\n";
    }

    // ── Run greedy scheduler ──
    // Mirrors Python: result = schedule_jobs(sample_jobs)
    ScheduleResult result = schedule_jobs(sample_jobs);

    // ── Print result ──
    // Mirrors Python: print_result(result)
    print_result(result);

    return 0;
}
