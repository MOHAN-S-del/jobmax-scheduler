cmake_minimum_required(VERSION 3.10)
project(JobScheduler)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add executable
add_executable(scheduler scheduler.cpp)

# Install target
install(TARGETS scheduler DESTINATION bin)
