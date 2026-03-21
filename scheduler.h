#ifndef SCHEDULER_H
#define SCHEDULER_H

#include "../models/job.h"
#include "../models/worker.h"
#include <vector>
#include <algorithm>
#include <string>
#include <ctime>

/**
 * scheduler.h — Greedy Job Scheduling Algorithm
 * ===============================================
 * Project : SkillSync — Greedy Job Scheduling Backend
 *
 * Algorithm : Greedy Job Sequencing with Deadlines
 *
 * Strategy:
 *   1. Sort jobs by deadline (earliest first) — EDF (Earliest Deadline First)
 *   2. Rank workers by score (rating, distance, cost)
 *   3. Assign each job to the best available worker
 *   4. Skip expired or unassignable jobs
 *
 * Time Complexity  : O(n log n) — dominated by sorting
 * Space Complexity : O(n)       — for assignment results
 */

// ── Worker Ranking System ─────────────────────────────────────
class WorkerRankingSystem {
public:
    /**
     * Rank workers using greedy scoring:
     * Score = (rating * 40) - (distance * 0.5) - (cost * 0.1)
     * Higher score = assigned first
     */
    static void rankWorkers(std::vector<Worker>& workers) {
        std::sort(workers.begin(), workers.end(),
            [](const Worker& a, const Worker& b) {
                // Primary: rating (higher is better)
                if (a.rating != b.rating)
                    return a.rating > b.rating;
                // Secondary: distance (closer is better)
                if (a.distance != b.distance)
                    return a.distance < b.distance;
                // Tertiary: cost (cheaper is better)
                return a.cost < b.cost;
            });
    }
};

// ── Job Scheduler ─────────────────────────────────────────────
class JobScheduler {
public:

    // Result of scheduling one job
    struct Assignment {
        int jobId;          // Job that was processed
        int workerId;       // Worker assigned (-1 if none)
        std::string status; // "scheduled", "expired", "overloaded", "no_skill_match"
    };

    /**
     * Main greedy scheduling function.
     *
     * @param jobs     List of jobs to schedule
     * @param workers  List of available workers
     * @param maxLoad  Maximum jobs per worker (default: 2)
     * @return         List of assignment results
     */
    static std::vector<Assignment> schedule(
        std::vector<Job>& jobs,
        std::vector<Worker>& workers,
        int maxLoad = 2)
    {
        std::vector<Assignment> results;
        std::time_t now = std::time(nullptr);

        // ── STEP 1: Sort jobs by deadline (Greedy Choice) ──
        // Earliest Deadline First ensures urgent jobs are handled first
        std::sort(jobs.begin(), jobs.end(),
            [](const Job& a, const Job& b) {
                return a.deadline < b.deadline;
            });

        // ── STEP 2: Rank workers by score ──
        WorkerRankingSystem::rankWorkers(workers);

        // ── STEP 3: Assign each job to best available worker ──
        for (auto& job : jobs) {

            // Skip expired jobs
            if (job.deadline < now) {
                job.status = "expired";
                results.push_back({ job.jobId, -1, "expired" });
                continue;
            }

            bool assigned = false;

            for (auto& worker : workers) {
                // Check if worker can take more jobs
                if (worker.currentLoad >= maxLoad) continue;

                // Check skill match if job requires specific skill
                if (!job.requiredSkill.empty() && !worker.skills.empty()) {
                    if (!worker.hasSkill(job.requiredSkill)) continue;
                }

                // ── GREEDY ASSIGNMENT ──
                worker.currentLoad++;
                job.assigned = true;
                job.assignedWorkerId = worker.workerId;
                job.status = "scheduled";

                results.push_back({ job.jobId, worker.workerId, "scheduled" });
                assigned = true;
                break;
            }

            if (!assigned) {
                // Check why — all workers overloaded or no skill match
                bool skillIssue = false;
                if (!job.requiredSkill.empty()) {
                    skillIssue = true;
                    for (const auto& w : workers) {
                        if (w.hasSkill(job.requiredSkill)) { skillIssue = false; break; }
                    }
                }
                std::string reason = skillIssue ? "no_skill_match" : "overloaded";
                job.status = reason;
                results.push_back({ job.jobId, -1, reason });
            }
        }

        return results;
    }

    /**
     * Get scheduling statistics.
     */
    static void printStats(const std::vector<Assignment>& results) {
        int scheduled = 0, expired = 0, overloaded = 0, noSkill = 0;
        for (const auto& r : results) {
            if (r.status == "scheduled")       scheduled++;
            else if (r.status == "expired")    expired++;
            else if (r.status == "no_skill_match") noSkill++;
            else                               overloaded++;
        }
        printf("\n── Scheduling Stats ──\n");
        printf("  Total Jobs   : %d\n", (int)results.size());
        printf("  Scheduled    : %d\n", scheduled);
        printf("  Expired      : %d\n", expired);
        printf("  Overloaded   : %d\n", overloaded);
        printf("  No Skill Match: %d\n", noSkill);
    }
};

#endif // SCHEDULER_H
