#include "mongoose.h"
#include "server/routes.h"
#include <iostream>

/**
 * SkillSync Backend Entry Point using Mongoose.
 */
int main() {
    struct mg_mgr mgr;
    mg_mgr_init(&mgr);

    SkillSyncRoutes routes;
    
    std::cout << "------------------------------------------" << std::endl;
    std::cout << "SkillSync: Greedy Job Scheduling Backend (Mongoose)" << std::endl;
    std::cout << "Server starting on http://localhost:8080" << std::endl;
    std::cout << "------------------------------------------" << std::endl;

    if (mg_http_listen(&mgr, "http://0.0.0.0:8080", SkillSyncRoutes::handle_request, &routes) == NULL) {
        std::cerr << "Could not start server on port 8080" << std::endl;
        return 1;
    }

    for (;;) mg_mgr_poll(&mgr, 1000);
    mg_mgr_free(&mgr);

    return 0;
}
