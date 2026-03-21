#ifndef JOB_H
#define JOB_H

#include <string>
#include <ctime>

/**
 * job.h — Job Model
 * =================
 * Project : SkillSync — Greedy Job Scheduling Backend
 *
 * Represents a single job request in the system.
 * Each job has a deadline, duration, required skill,
 * and tracks whether it has been assigned to a worker.
 */

struct Job {
    int jobId;                  // Unique job identifier
    std::time_t deadline;       // Unix timestamp — job must be done before this
    int duration;               // Duration in minutes
    std::string requiredSkill;  // Skill needed (e.g. "Plumber", "Carpenter")
    bool assigned;              // Whether job has been assigned to a worker
    int assignedWorkerId;       // ID of assigned worker (-1 if unassigned)
    std::string status;         // "pending", "scheduled", "expired", "overloaded"
    std::string createdAt;      // When job was posted

    // ── Constructor ──────────────────────────────────────────
    Job(int id, std::time_t dl, int dur, std::string skill)
        : jobId(id),
          deadline(dl),
          duration(dur),
          requiredSkill(skill),
          assigned(false),
          assignedWorkerId(-1),
          status("pending") {
        // Record creation time
        std::time_t now = std::time(nullptr);
        char buf[20];
        std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&now));
        createdAt = std::string(buf);
    }

    // ── Helper: Check if job is expired ──────────────────────
    bool isExpired() const {
        return std::time(nullptr) > deadline;
    }

    // ── Helper: Get deadline as formatted string ──────────────
    std::string getDeadlineStr() const {
        char buf[20];
        std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&deadline));
        return std::string(buf);
    }

    // ── Helper: Get remaining time in seconds ─────────────────
    long long getRemainingSeconds() const {
        long long remaining = (long long)deadline - (long long)std::time(nullptr);
        return remaining > 0 ? remaining : 0;
    }
};

#endif // JOB_H
