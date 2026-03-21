#ifndef ROUTES_H
#define ROUTES_H

#include "mongoose.h"
#include "json.hpp"
#include "../models/job.h"
#include "../models/worker.h"
#include "../algorithms/scheduler.h"
#include <vector>
#include <mutex>
#include <string>

using json = nlohmann::json;

/**
 * REST API Routes for SkillSync using Mongoose.
 */
class SkillSyncRoutes {
private:
    std::vector<Job> jobs;
    std::vector<Worker> workers;
    std::mutex dataMutex;

public:
    static void handle_request(struct mg_connection *c, int ev, void *ev_data, void *fn_data) {
        if (ev == MG_EV_HTTP_MSG) {
            struct mg_http_message *hm = (struct mg_http_message *)ev_data;
            SkillSyncRoutes *routes = (SkillSyncRoutes *)fn_data;

            // CORS headers
            mg_http_reply(c, 200, "Access-Control-Allow-Origin: *\r\n"
                                 "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
                                 "Access-Control-Allow-Headers: Content-Type\r\n", "");

            if (mg_http_match_uri(hm, "/add_job") && mg_vcasecmp(&hm->method, "POST") == 0) {
                try {
                    auto data = json::parse(std::string(hm->body.ptr, hm->body.len));
                    std::lock_guard<std::mutex> lock(routes->dataMutex);
                    routes->jobs.emplace_back(data["jobId"].get<int>(), (std::time_t)data["deadline"].get<int>(), 
                                               data["duration"].get<int>(), data["requiredSkill"].get<std::string>());
                    mg_http_reply(c, 201, "Content-Type: text/plain\r\n", "Job Added Successfully");
                } catch (...) { mg_http_reply(c, 400, "", "Invalid JSON"); }

            } else if (mg_http_match_uri(hm, "/jobs") && mg_vcasecmp(&hm->method, "GET") == 0) {
                std::lock_guard<std::mutex> lock(routes->dataMutex);
                json jobList = json::array();
                for (const auto& job : routes->jobs) {
                    jobList.push_back({{"jobId", job.jobId}, {"deadline", (int)job.deadline}, {"duration", job.duration}, 
                                        {"requiredSkill", job.requiredSkill}, {"assigned", job.assigned}, {"assignedWorkerId", job.assignedWorkerId}});
                }
                mg_http_reply(c, 200, "Content-Type: application/json\r\n", "%s", jobList.dump().c_str());

            } else if (mg_http_match_uri(hm, "/add_worker") && mg_vcasecmp(&hm->method, "POST") == 0) {
                try {
                    auto data = json::parse(std::string(hm->body.ptr, hm->body.len));
                    std::lock_guard<std::mutex> lock(routes->dataMutex);
                    std::vector<std::string> skills;
                    if (data.contains("skills")) { for (const auto& s : data["skills"]) skills.push_back(s.get<std::string>()); }
                    routes->workers.emplace_back(data["workerId"].get<int>(), data["rating"].get<double>(), 
                                                  data["distance"].get<double>(), data["cost"].get<double>(), 
                                                  data["currentLoad"].get<int>(), skills);
                    mg_http_reply(c, 201, "Content-Type: text/plain\r\n", "Worker Added Successfully");
                } catch (...) { mg_http_reply(c, 400, "", "Invalid JSON"); }

            } else if (mg_http_match_uri(hm, "/workers") && mg_vcasecmp(&hm->method, "GET") == 0) {
                std::lock_guard<std::mutex> lock(routes->dataMutex);
                json workerList = json::array();
                for (const auto& w : routes->workers) {
                    workerList.push_back({{"workerId", w.workerId}, {"rating", w.rating}, {"distance", w.distance}, {"cost", w.cost}, {"currentLoad", w.currentLoad}});
                }
                mg_http_reply(c, 200, "Content-Type: application/json\r\n", "%s", workerList.dump().c_str());

            } else if (mg_http_match_uri(hm, "/schedule") && mg_vcasecmp(&hm->method, "POST") == 0) {
                std::lock_guard<std::mutex> lock(routes->dataMutex);
                if (routes->jobs.empty() || routes->workers.empty()) {
                    mg_http_reply(c, 400, "", "No data available");
                } else {
                    auto assignments = JobScheduler::schedule(routes->jobs, routes->workers);
                    json res = json::array();
                    for (const auto& a : assignments) res.push_back({{"jobId", a.jobId}, {"assignedWorker", a.workerId}, {"status", a.status}});
                    mg_http_reply(c, 200, "Content-Type: application/json\r\n", "%s", res.dump().c_str());
                }

            } else if (mg_http_match_uri(hm, "/status") && mg_vcasecmp(&hm->method, "GET") == 0) {
                std::lock_guard<std::mutex> lock(routes->dataMutex);
                json status = {{"total_jobs", (int)routes->jobs.size()}, {"total_workers", (int)routes->workers.size()}, {"status", "operational"}};
                mg_http_reply(c, 200, "Content-Type: application/json\r\n", "%s", status.dump().c_str());

            } else {
                mg_http_reply(c, 404, "", "Not Found");
            }
        }
    }
};

#endif // ROUTES_H
