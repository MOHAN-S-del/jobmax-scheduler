#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <cstring>
#include <stdlib.h>
#include <sstream>
#include <iomanip>
#include <numeric>

using namespace std;

// ─── Helper: Calculate days until deadline ────────────
int calculateDaysUntilDeadline(const string& deadline_str, string& error_msg) {
    struct tm deadline_tm = {};
    memset(&deadline_tm, 0, sizeof(struct tm));
    istringstream ss(deadline_str);
    
    // Try ISO datetime format
    ss >> get_time(&deadline_tm, "%Y-%m-%dT%H:%M:%S");
    
    if (ss.fail()) {
        ss.clear();
        ss.str(deadline_str.substr(0, 10));
        ss >> get_time(&deadline_tm, "%Y-%m-%d");
        if (ss.fail()) {
            error_msg = "Invalid date format. Expected YYYY-MM-DD.";
            return -1;
        }
    }
    
    time_t deadline_time = mktime(&deadline_tm);
    time_t now = time(nullptr);
    
    struct tm* now_tm = localtime(&now);
    struct tm today_tm = *now_tm;
    today_tm.tm_hour = 0;
    today_tm.tm_min = 0;
    today_tm.tm_sec = 0;
    time_t today_start = mktime(&today_tm);

    if (deadline_time < today_start) {
        error_msg = "Invalid deadline: Please enter a future date.";
        return -2;
    }
    
    double seconds_diff = difftime(deadline_time, now);
    int days_diff = static_cast<int>(seconds_diff / (60 * 60 * 24));
    
    return max(0, days_diff + 1);
}

// ─── Job Structure ────────────────────────────────────
struct Job {
    int id;
    string job_type;
    string name;
    string deadline;
    int profit;
    int days_deadline;
};

// ─── DSU for Optimization ─────────────────────────────
struct DSU {
    vector<int> parent;
    DSU(int n) {
        parent.resize(n + 1);
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int i) {
        if (i == parent[i]) return i;
        return parent[i] = find(parent[i]);
    }
    void unite(int i, int j) {
        parent[i] = j;
    }
};

// ─── Schedule Result Structure ────────────────────────
struct ScheduledJob {
    int day;
    string name;
    int profit;
    string job_type;
};

struct ScheduleResult {
    vector<ScheduledJob> scheduled;
    vector<Job> skipped;
    int total_profit;
    vector<string> steps;
};

// ─── Optimized Greedy Job Scheduling Algorithm ────────
ScheduleResult scheduleJobs(vector<Job>& jobs) {
    ScheduleResult result;
    result.total_profit = 0;

    if (jobs.empty()) {
        result.steps.push_back("No jobs to schedule");
        return result;
    }

    result.steps.push_back("Step 1: Sorting " + to_string(jobs.size()) + " jobs by profit (descending)");
    sort(jobs.begin(), jobs.end(), [](const Job& a, const Job& b) {
        return a.profit > b.profit;
    });

    int max_deadline = 0;
    for (const auto& job : jobs) {
        if (job.days_deadline > 0)
            max_deadline = max(max_deadline, job.days_deadline);
    }
    
    // Cap max deadline to something reasonable for slots (e.g., 365 days)
    max_deadline = min(max_deadline, 365);
    
    result.steps.push_back("Step 2: Maximum deadline is " + to_string(max_deadline) + " days");
    result.steps.push_back("Step 3: Initialized " + to_string(max_deadline) + " time slots");

    DSU dsu(max_deadline);
    result.steps.push_back("Step 4: Scheduling jobs in profit order");

    for (const auto& job : jobs) {
        if (job.days_deadline == -2) {
            result.skipped.push_back(job);
            result.steps.push_back("  ✗ Skipped '" + job.name + "' (₹" + to_string(job.profit) + ") - Deadline was in the past");
            continue;
        }

        int available_slot = dsu.find(min(job.days_deadline, max_deadline));
        
        if (available_slot > 0) {
            dsu.unite(available_slot, available_slot - 1);
            result.scheduled.push_back({available_slot, job.name, job.profit, job.job_type});
            result.total_profit += job.profit;
            result.steps.push_back("  ✓ Scheduled '" + job.name + "' (₹" + to_string(job.profit) + ") on day " + to_string(available_slot));
        } else {
            result.skipped.push_back(job);
            result.steps.push_back("  ✗ Skipped '" + job.name + "' (₹" + to_string(job.profit) + ") - no available slot before deadline");
        }
    }

    result.steps.push_back("Step 5: Scheduling complete. Total profit: ₹" + to_string(result.total_profit));
    return result;
}

// ─── Robust JSON Parser ───────────────────────────────
string getJsonField(const string& json, const string& field) {
    size_t fpos = json.find("\"" + field + "\"");
    if (fpos == string::npos) return "";
    
    size_t colon = json.find(":", fpos);
    if (colon == string::npos) return "";
    
    size_t start = json.find_first_not_of(" \t\n\r", colon + 1);
    if (start == string::npos) return "";
    
    if (json[start] == '\"') {
        size_t end = json.find("\"", start + 1);
        if (end == string::npos) return "";
        return json.substr(start + 1, end - start - 1);
    } else {
        size_t end = json.find_first_of(",}\n\r\t ", start);
        if (end == string::npos) end = json.length();
        return json.substr(start, end - start);
    }
}

bool parseJobsFromJSON(const string& json_str, vector<Job>& jobs, string& error_msg) {
    jobs.clear();
    size_t pos = 0;

    while ((pos = json_str.find("{", pos)) != string::npos) {
        size_t end_pos = json_str.find("}", pos);
        if (end_pos == string::npos) break;
        
        string job_obj = json_str.substr(pos, end_pos - pos + 1);
        
        Job job;
        string id_s = getJsonField(job_obj, "id");
        job.id = id_s.empty() ? 0 : stoi(id_s);
        job.job_type = getJsonField(job_obj, "job_type");
        job.name = getJsonField(job_obj, "name");
        job.deadline = getJsonField(job_obj, "deadline");
        string profit_s = getJsonField(job_obj, "profit");
        job.profit = profit_s.empty() ? 0 : stoi(profit_s);
        
        if (!job.deadline.empty()) {
            job.days_deadline = calculateDaysUntilDeadline(job.deadline, error_msg);
            if (job.days_deadline == -1) return false;
        } else {
            job.days_deadline = 0;
        }

        if (!job.name.empty() && job.profit >= 0) {
            jobs.push_back(job);
        }
        
        pos = end_pos + 1;
    }
    return !jobs.empty();
}

// ─── Output result as JSON ────────────────────────────
string escapeJson(const string& s) {
    string out;
    for (char c : s) {
        if (c == '"') out += "\\\"";
        else if (c == '\\') out += "\\\\";
        else if (c == '\b') out += "\\b";
        else if (c == '\f') out += "\\f";
        else if (c == '\n') out += "\\n";
        else if (c == '\r') out += "\\r";
        else if (c == '\t') out += "\\t";
        else out += c;
    }
    return out;
}

string resultToJSON(const ScheduleResult& result) {
    stringstream ss;
    ss << "{\n";
    ss << "  \"scheduled\": [\n";
    for (size_t i = 0; i < result.scheduled.size(); i++) {
        ss << "    {\"day\": " << result.scheduled[i].day 
           << ", \"name\": \"" << escapeJson(result.scheduled[i].name) << "\""
           << ", \"profit\": " << result.scheduled[i].profit
           << ", \"job_type\": \"" << escapeJson(result.scheduled[i].job_type) << "\"}";
        if (i < result.scheduled.size() - 1) ss << ",";
        ss << "\n";
    }
    ss << "  ],\n";
    ss << "  \"skipped\": [\n";
    for (size_t i = 0; i < result.skipped.size(); i++) {
        ss << "    {\"name\": \"" << escapeJson(result.skipped[i].name) << "\""
           << ", \"profit\": " << result.skipped[i].profit << "}";
        if (i < result.skipped.size() - 1) ss << ",";
        ss << "\n";
    }
    ss << "  ],\n";
    ss << "  \"steps\": [\n";
    for (size_t i = 0; i < result.steps.size(); i++) {
        ss << "    \"" << escapeJson(result.steps[i]) << "\"";
        if (i < result.steps.size() - 1) ss << ",";
        ss << "\n";
    }
    ss << "  ],\n";
    ss << "  \"total_profit\": " << result.total_profit << "\n";
    ss << "}\n";
    return ss.str();
}

int main(int argc, char* argv[]) {
    string json_input;
    if (argc >= 2) {
        json_input = argv[1];
    } else {
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
    string error_msg;
    if (!parseJobsFromJSON(json_input, jobs, error_msg)) {
        if (!error_msg.empty()) {
            cout << "{\n  \"error\": \"" << escapeJson(error_msg) << "\",\n  \"scheduled\": [],\n  \"skipped\": [],\n  \"total_profit\": 0,\n  \"steps\": [\"Error: " << escapeJson(error_msg) << "\"]\n}\n";
            return 0;
        }
        cerr << "Failed to parse jobs from JSON" << endl;
        return 1;
    }

    ScheduleResult result = scheduleJobs(jobs);
    cout << resultToJSON(result);
    return 0;
}
