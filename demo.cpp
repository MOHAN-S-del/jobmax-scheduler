#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <ctime>
#include <iomanip>
#include <map>

// --- Models ---

struct Job {
    int jobId;
    std::time_t deadline;
    int duration;
    std::string requiredSkill;
    bool assigned = false;
    int assignedWorkerId = -1;

    Job(int id, std::time_t dl, int dur, std::string skill)
        : jobId(id), deadline(dl), duration(dur), requiredSkill(skill) {}
};

struct Worker {
    int workerId;
    double rating;
    double distance;
    double cost;
    int currentLoad;

    Worker(int id, double r, double dist, double c, int load)
        : workerId(id), rating(r), distance(dist), cost(c), currentLoad(load) {}
};

// --- In-Memory Storage ---
std::vector<Job> g_jobs;
std::vector<Worker> g_workers;

// --- Algorithms ---

class WorkerRankingSystem {
public:
    static void rankWorkers(std::vector<Worker>& workers) {
        std::sort(workers.begin(), workers.end(), [](const Worker& a, const Worker& b) {
            if (a.rating != b.rating) return a.rating > b.rating;
            if (a.distance != b.distance) return a.distance < b.distance;
            return a.cost < b.cost;
        });
    }
};

class JobScheduler {
public:
    struct Assignment {
        int jobId;
        int workerId;
        std::string status;
    };

    static std::vector<Assignment> schedule(std::vector<Job>& jobs, std::vector<Worker>& workers, int maxLoad = 2) {
        std::vector<Assignment> results;
        std::time_t now = std::time(nullptr);

        std::sort(jobs.begin(), jobs.end(), [](const Job& a, const Job& b) {
            return a.deadline < b.deadline;
        });

        WorkerRankingSystem::rankWorkers(workers);

        for (auto& job : jobs) {
            if (job.deadline < now) {
                results.push_back({job.jobId, -1, "expired"});
                continue;
            }

            bool assigned = false;
            for (auto& worker : workers) {
                if (worker.currentLoad < maxLoad) {
                    worker.currentLoad++;
                    job.assigned = true;
                    job.assignedWorkerId = worker.workerId;
                    results.push_back({job.jobId, worker.workerId, "scheduled"});
                    assigned = true;
                    break;
                }
            }

            if (!assigned) {
                results.push_back({job.jobId, -1, "overloaded/no_workers"});
            }
        }
        return results;
    }
};

// --- Main Demo CLI ---

void printStatus() {
    std::cout << "\n--- System Status ---\n";
    std::cout << "Total Jobs: " << g_jobs.size() << "\n";
    std::cout << "Total Workers: " << g_workers.size() << "\n";
}

void addJob() {
    int id, dur;
    std::string skill;
    std::cout << "Enter Job ID: "; std::cin >> id;
    std::cout << "Enter Duration (min): "; std::cin >> dur;
    std::cout << "Enter Skill: "; std::cin >> skill;
    g_jobs.emplace_back(id, std::time(nullptr) + 3600, dur, skill);
    std::cout << "Job added successfully!\n";
}

void addWorker() {
    int id;
    double r, d, c;
    std::cout << "Enter Worker ID: "; std::cin >> id;
    std::cout << "Enter Rating (1-5): "; std::cin >> r;
    std::cout << "Enter Distance (km): "; std::cin >> d;
    std::cout << "Enter Cost: "; std::cin >> c;
    g_workers.emplace_back(id, r, d, c, 0);
    std::cout << "Worker added successfully!\n";
}

void runScheduler() {
    if (g_jobs.empty() || g_workers.empty()) {
        std::cout << "Need both jobs and workers to schedule!\n";
        return;
    }
    auto assignments = JobScheduler::schedule(g_jobs, g_workers);
    std::cout << "\nAssignments:\n";
    for (const auto& a : assignments) {
        std::cout << "Job " << a.jobId << " -> Worker " << (a.workerId == -1 ? "None" : std::to_string(a.workerId)) << " [" << a.status << "]\n";
    }
}

int main() {
    int choice;
    while (true) {
        std::cout << "\n=== SkillSync CLI ===\n";
        std::cout << "1. Add Job\n";
        std::cout << "2. Add Worker\n";
        std::cout << "3. Run Scheduler\n";
        std::cout << "4. Status\n";
        std::cout << "5. Exit\n";
        std::cout << "Choice: ";
        if (!(std::cin >> choice)) break;
        if (choice == 1) addJob();
        else if (choice == 2) addWorker();
        else if (choice == 3) runScheduler();
        else if (choice == 4) printStatus();
        else break;
    }
    return 0;
}

