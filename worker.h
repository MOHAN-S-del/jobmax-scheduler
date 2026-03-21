#ifndef WORKER_H
#define WORKER_H

#include <string>
#include <vector>

/**
 * worker.h — Worker Model
 * ========================
 * Project : SkillSync — Greedy Job Scheduling Backend
 *
 * Represents a skilled worker available for job assignments.
 * Workers are ranked by rating, distance, and cost.
 * Each worker has a maximum load (jobs they can handle at once).
 */

struct Worker {
    int workerId;                       // Unique worker identifier
    std::string name;                   // Worker's name
    double rating;                      // Rating out of 5.0
    double distance;                    // Distance from job location (km)
    double cost;                        // Cost per job (rupees)
    int currentLoad;                    // Number of jobs currently assigned
    int maxLoad;                        // Maximum jobs worker can handle
    std::vector<std::string> skills;    // List of skills e.g. {"Plumber", "Carpenter"}
    bool available;                     // Whether worker is currently available
    std::string workerType;             // Primary worker type

    // ── Constructor (basic) ───────────────────────────────────
    Worker(int id, double r, double dist, double c, int load)
        : workerId(id),
          name("Worker " + std::to_string(id)),
          rating(r),
          distance(dist),
          cost(c),
          currentLoad(load),
          maxLoad(3),
          available(true),
          workerType("General") {}

    // ── Constructor (with skills) ─────────────────────────────
    Worker(int id, double r, double dist, double c, int load, std::vector<std::string> sk)
        : workerId(id),
          name("Worker " + std::to_string(id)),
          rating(r),
          distance(dist),
          cost(c),
          currentLoad(load),
          maxLoad(3),
          skills(sk),
          available(true),
          workerType(sk.empty() ? "General" : sk[0]) {}

    // ── Helper: Check if worker can take more jobs ────────────
    bool canTakeJob() const {
        return available && (currentLoad < maxLoad);
    }

    // ── Helper: Check if worker has a specific skill ──────────
    bool hasSkill(const std::string& skill) const {
        for (const auto& s : skills) {
            if (s == skill) return true;
        }
        return false;
    }

    // ── Helper: Calculate worker score for ranking ────────────
    // Higher score = better worker
    // Formula: (rating * 40) - (distance * 0.5) - (cost * 0.1)
    double getScore() const {
        return (rating * 40.0) - (distance * 0.5) - (cost * 0.1);
    }

    // ── Helper: Assign a job to this worker ───────────────────
    void assignJob() {
        currentLoad++;
        if (currentLoad >= maxLoad) available = false;
    }

    // ── Helper: Release a job from this worker ────────────────
    void releaseJob() {
        if (currentLoad > 0) currentLoad--;
        available = true;
    }
};

#endif // WORKER_H
