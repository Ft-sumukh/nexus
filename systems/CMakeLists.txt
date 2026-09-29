# ==============================================================================
# TITAN Systems Layer — CMake Configuration
# ==============================================================================

# Runtime / Hardware Probe Library
add_library(titan_systems STATIC
    runtime/src/hardware_probe.cpp
)

target_include_directories(titan_systems PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/runtime/include
)

target_compile_features(titan_systems PUBLIC cxx_std_20)

if (TITAN_CUDA_ENABLED)
    target_compile_definitions(titan_systems PUBLIC TITAN_CUDA_ENABLED=1)
    target_link_libraries(titan_systems PUBLIC CUDA::cudart)
else()
    target_compile_definitions(titan_systems PUBLIC TITAN_CPU_ONLY=1)
endif()

# Hardware Probe Test Executable
add_executable(test_hardware_probe
    runtime/tests/test_hardware_probe.cpp
)

target_link_libraries(test_hardware_probe PRIVATE titan_systems)
target_compile_features(test_hardware_probe PRIVATE cxx_std_20)

add_test(NAME TestHardwareProbe COMMAND test_hardware_probe)
