cmake_minimum_required(VERSION 3.14)
project(SkillSyncBackend)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Fetch Crow framework from GitHub
include(FetchContent)
FetchContent_Declare(
    crow
    GIT_REPOSITORY https://github.com/CrowCpp/Crow.git
    GIT_TAG v1.0+5 # or specify a stable version tag
)
FetchContent_MakeAvailable(crow)

# Include directories
include_directories(${CMAKE_SOURCE_DIR})

# Add the main executable
add_executable(SkillSyncBackend main.cpp)

# Link Crow
target_link_libraries(SkillSyncBackend PRIVATE Crow::Crow)

# Handle Asio/Threads dependency (usually included via Crow)
find_package(Threads REQUIRED)
target_link_libraries(SkillSyncBackend PRIVATE Threads::Threads)

# Additional configurations for Windows
if(WIN32)
    target_compile_definitions(SkillSyncBackend PRIVATE _WIN32_WINNT=0x0601)
endif()

message(STATUS "SkillSync Backend configured successfully.")
