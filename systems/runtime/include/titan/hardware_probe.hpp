#pragma once

#include <cstdint>
#include <string>
#include <iostream>

namespace titan {

/**
 * Encapsulates detected host hardware metrics.
 */
struct HardwareInfo {
    std::string cpu_architecture;
    unsigned int logical_cores{0};
    unsigned int physical_cores{0};
    uint64_t total_physical_memory_bytes{0};
    uint64_t available_physical_memory_bytes{0};
    bool cuda_available{false};
    std::string gpu_device_name{"None"};
    int gpu_device_count{0};
    std::string build_mode{"CPU_ONLY"};
};

/**
 * Dynamically probes the host machine for CPU, memory, and accelerator capabilities.
 */
class HardwareProbe {
public:
    /**
     * Inspects host hardware without assuming or hardcoding values.
     */
    static HardwareInfo probe();

    /**
     * Outputs a formatted diagnostic summary to the given stream.
     */
    static void print_summary(std::ostream& os = std::cout);
};

} // namespace titan
