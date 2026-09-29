cmake_minimum_required(VERSION 3.25)

project(nexus_titan
    VERSION 0.1.0
    DESCRIPTION "NEXUS TITAN — AI Systems, Runtime & High-Performance Computing Laboratory"
    LANGUAGES CXX
)

# Standard C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Enable CTest
enable_testing()

# Compiler Warning Flags
if (MSVC)
    add_compile_options(/W4 /permissive-)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ------------------------------------------------------------------------------
# Hardware Capability Probing (CUDA vs CPU-Only)
# ------------------------------------------------------------------------------
option(TITAN_ENABLE_CUDA "Enable CUDA GPU Acceleration" AUTO)

include(CheckLanguage)
check_language(CUDA)

if (CMAKE_CUDA_COMPILER AND NOT TITAN_ENABLE_CUDA STREQUAL "OFF")
    enable_language(CUDA)
    set(TITAN_CUDA_ENABLED ON CACHE BOOL "CUDA Enabled" FORCE)
    message(STATUS "[NEXUS TITAN] CUDA detected: ${CMAKE_CUDA_COMPILER}. GPU Engine enabled.")
else()
    set(TITAN_CUDA_ENABLED OFF CACHE BOOL "CUDA Enabled" FORCE)
    message(STATUS "[NEXUS TITAN] CUDA compiler not detected or disabled. Compiling in CPU-ONLY Mode with software fallbacks.")
endif()

# ------------------------------------------------------------------------------
# Subsystems
# ------------------------------------------------------------------------------
add_subdirectory(systems)
