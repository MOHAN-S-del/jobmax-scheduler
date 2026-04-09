#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <cstring>
#include <stdlib.h>
#include <sstream>
#include <iomanip>

using namespace std;

// ─── Helper: Calculate days until deadline ────────────
int calculateDaysUntilDeadline(const string& deadline_str) {
    // Parse ISO datetime string (e.g., "2024-01-15T10:00:00")
    // Return days until deadline from current time
    
    struct tm deadline_tm = {};
    istringstream ss(deadline_str);
    ss >> get_time(&deadline_tm, "%Y-%m-%dT%H:%M:%S");
    
    if (ss.fail()) {
        // Fallback: try date only format
        ss.clear();
        ss.str(deadline_str.substr(0, 10)); // Take date part only
        ss >> get_time(&deadline_tm, "%Y-%m-%d");
        if (ss.fail()) {
            return 7; // Default fallback
        }
    }
    
    time_t deadline_time = mktime(&deadline_tm);
    time_t now = time(nullptr);
    
    double seconds_diff = difftime(deadline_time, now);
    int days_diff = static_cast<int>(seconds_diff / (60 * 60 * 24));
    
    return max(1, days_diff); // At least 1 day
}

// ─── Job Structure ────────────────────────────────────
struct Job {
    int id;
    string job_type;
    string name;
    string deadline;  // ISO datetime string
    int profit;
    int days_deadline; // calculated days until deadline
};

// ─── Schedule Result Structure ────────────────────────
struct ScheduleResult {
    vector<pair<int, string>> scheduled;  // {slot, job_name}
    vector<Job> skipped;
    int total_profit;
    vector<string> steps;  // Algorithm execution steps
};

// ─── Greedy Job Scheduling Algorithm ──────────────────
ScheduleResult scheduleJobs(vector<Job>& jobs) {
    ScheduleResult result;
    result.total_profit = 0;

    if (jobs.empty()) {
        result.steps.push_back("No jobs to schedule");
        return result;
    }

    result.steps.push_back("Step 1: Sorting " + to_string(jobs.size()) + " jobs by profit (descending)");
    // ── STEP 1: Sort jobs by profit in descending order ──
    sort(jobs.begin(), jobs.end(), [](const Job& a, const Job& b) {
        return a.profit > b.profit;
    });

    // ── STEP 2: Find maximum deadline ──
    int max_deadline = 0;
    for (const auto& job : jobs) {
        max_deadline = max(max_deadline, job.days_deadline);
    }
    result.steps.push_back("Step 2: Maximum deadline is " + to_string(max_deadline) + " days");

    // ── STEP 3: Initialize slots array (false = empty, true = occupied) ──
    vector<bool> slots(max_deadline, false);
    vector<string> slot_jobs(max_deadline, "");
    result.steps.push_back("Step 3: Initialized " + to_string(max_deadline) + " time slots");

    // ── STEP 4: For each job (in order of decreasing profit) ──
    result.steps.push_back("Step 4: Scheduling jobs in profit order");
    for (const auto& job : jobs) {
        // Try to place job in latest available slot before deadline
        bool placed = false;
        int available_slot = -1;
        
        for (int t = min(job.days_deadline, max_deadline) - 1; t >= 0; t--) {
            if (!slots[t]) {
                available_slot = t;
                break;
            }
        }
        
        if (available_slot != -1) {
            // Slot is free, place job here
            slots[available_slot] = true;
            slot_jobs[available_slot] = job.name;
            result.scheduled.push_back({available_slot + 1, job.name});
            result.total_profit += job.profit;
            placed = true;
            result.steps.push_back("  ✓ Scheduled '" + job.name + "' (₹" + to_string(job.profit) + ") on day " + to_string(available_slot + 1));
        }

        if (!placed) {
            result.skipped.push_back(job);
            result.steps.push_back("  ✗ Skipped '" + job.name + "' (₹" + to_string(job.profit) + ") - no available slot before deadline");
        }
    }

    result.steps.push_back("Step 5: Scheduling complete. Total profit: ₹" + to_string(result.total_profit));
    return result;
}

// ─── Simple JSON Parser for input ─────────────────────
bool parseJobsFromJSON(const string& json_str, vector<Job>& jobs) {
    // Simple parser for JSON array of jobs
    // Format: [{"id":1,"job_type":"Web Development","name":"Project","deadline":"2024-01-01T10:00","profit":500},...]
    
    jobs.clear();
    size_t pos = 0;

    while ((pos = json_str.find("{", pos)) != string::npos) {
        Job job;
        job.id = 0;
        job.days_deadline = 7; // default
        job.profit = 0;
        job.name = "";
        job.job_type = "";
        job.deadline = "";
        
        size_t end_pos = json_str.find("}", pos);
        string job_str = json_str.substr(pos, end_pos - pos + 1);
        
        // Parse id
        size_t id_pos = job_str.find("\"id\"");
        if (id_pos != string::npos) {
            size_t colon = job_str.find(":", id_pos);
            size_t comma = job_str.find(",", colon);
            string id_str = job_str.substr(colon + 1, comma - colon - 1);
            id_str.erase(remove_if(id_str.begin(), id_str.end(), ::isspace), id_str.end());
            job.id = stoi(id_str);
        }

        // Parse job_type
        size_t type_pos = job_str.find("\"job_type\"");
        if (type_pos != string::npos) {
            size_t colon = job_str.find(":", type_pos);
            size_t first_quote = job_str.find("\"", colon);
            size_t second_quote = job_str.find("\"", first_quote + 1);
            job.job_type = job_str.substr(first_quote + 1, second_quote - first_quote - 1);
        }

        // Parse name
        size_t name_pos = job_str.find("\"name\"");
        if (name_pos != string::npos) {
            size_t colon = job_str.find(":", name_pos);
            size_t first_quote = job_str.find("\"", colon);
            size_t second_quote = job_str.find("\"", first_quote + 1);
            job.name = job_str.substr(first_quote + 1, second_quote - first_quote - 1);
        }

        // Parse deadline (datetime string)
        size_t deadline_pos = job_str.find("\"deadline\"");
        if (deadline_pos != string::npos) {
            size_t colon = job_str.find(":", deadline_pos);
            size_t first_quote = job_str.find("\"", colon);
            size_t second_quote = job_str.find("\"", first_quote + 1);
            job.deadline = job_str.substr(first_quote + 1, second_quote - first_quote - 1);
            
            // Calculate actual days until deadline
            job.days_deadline = calculateDaysUntilDeadline(job.deadline);
        }

        // Parse profit
        size_t profit_pos = job_str.find("\"profit\"");
        if (profit_pos != string::npos) {
            size_t colon = job_str.find(":", profit_pos);
            size_t comma = job_str.find(",", colon);
            if (comma == string::npos) comma = job_str.find("}", colon);
            string profit_str = job_str.substr(colon + 1, comma - colon - 1);
            profit_str.erase(remove_if(profit_str.begin(), profit_str.end(), ::isspace), profit_str.end());
            job.profit = stoi(profit_str);
        }

        if (!job.name.empty() && job.profit > 0) {
            jobs.push_back(job);
        }
        
        pos = end_pos + 1;
    }

    return !jobs.empty();
}

// ─── Output result as JSON ────────────────────────────
string resultToJSON(const ScheduleResult& result) {
    string json = "{\n";
    json += "  \"scheduled\": [\n";
    
    for (size_t i = 0; i < result.scheduled.size(); i++) {
        json += "    {\"day\": " + to_string(result.scheduled[i].first) + 
                ", \"job\": \"" + result.scheduled[i].second + "\"}";
        if (i < result.scheduled.size() - 1) json += ",";
        json += "\n";
    }
    
    json += "  ],\n";
    json += "  \"skipped\": [\n";
    
    for (size_t i = 0; i < result.skipped.size(); i++) {
        json += "    {\"name\": \"" + result.skipped[i].name + "\", \"profit\": " + 
                to_string(result.skipped[i].profit) + "}";
        if (i < result.skipped.size() - 1) json += ",";
        json += "\n";
    }
    
    json += "  ],\n";
    json += "  \"steps\": [\n";
    
    for (size_t i = 0; i < result.steps.size(); i++) {
        json += "    \"" + result.steps[i] + "\"";
        if (i < result.steps.size() - 1) json += ",";
        json += "\n";
    }
    
    json += "  ],\n";
    json += "  \"total_profit\": " + to_string(result.total_profit) + "\n";
    json += "}\n";
    
    return json;
}

// ─── Main ─────────────────────────────────────────────
int main(int argc, char* argv[]) {
    string json_input;
    
    // Read JSON from stdin (preferred) or command line argument
    if (argc >= 2) {
        json_input = argv[1];
    } else {
        // Read entire stdin
        string line;
        while (getline(cin, line)) {
            json_input += line;
        }
    }

    if (json_input.empty()) {
        cerr << "No JSON input provided" << endl;
        return 1;
    }

    vector<Job> jobs;

    if (!parseJobsFromJSON(json_input, jobs)) {
        cerr << "Failed to parse jobs from JSON" << endl;
        return 1;
    }

    // Run greedy algorithm
    ScheduleResult result = scheduleJobs(jobs);

    // Output as JSON
    cout << resultToJSON(result);

    return 0;
}
