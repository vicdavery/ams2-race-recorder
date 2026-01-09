cmake_minimum_required(VERSION 3.15)
project(AMS2RaceRecorder)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Windows-specific settings
if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /O2")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
endif()

# Find required packages
find_package(SQLite3 REQUIRED)

# Add source files
add_executable(ams2_recorder
    src/main.cpp
    src/shared_memory.cpp
    src/database.cpp
    src/race_session.cpp
)

# Link libraries
target_link_libraries(ams2_recorder
    SQLite3::SQLite3
)

# Include directories
target_include_directories(ams2_recorder PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Output directory
set_target_properties(ams2_recorder PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
