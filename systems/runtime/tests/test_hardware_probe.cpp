#include "titan/hardware_probe.hpp"

#include <cassert>
#include <iostream>
#include <sstream>

int main() {
    std::cout << "[TEST] Running titan::HardwareProbe test...\n";

    titan::HardwareInfo info = titan::HardwareProbe::probe();

    // Verification 1: Logical cores must be positive
    assert(info.logical_cores > 0);
    std::cout << "  ✓ Logical cores detected: " << info.logical_cores << "\n";

    // Verification 2: Physical cores must be positive and not exceed logical cores
    assert(info.physical_cores > 0);
    assert(info.physical_cores <= info.logical_cores);
    std::cout << "  ✓ Physical cores detected: " << info.physical_cores << "\n";

    // Verification 3: Total RAM must be > 0 bytes
    assert(info.total_physical_memory_bytes > 0);
    std::cout << "  ✓ Total RAM: " << (info.total_physical_memory_bytes / (1024 * 1024)) << " MB\n";

    // Verification 4: Architecture string must not be empty
    assert(!info.cpu_architecture.empty());
    std::cout << "  ✓ Architecture: " << info.cpu_architecture << "\n";

    // Verification 5: In CPU-only build, CUDA must be marked unavailable
#if !defined(TITAN_CUDA_ENABLED)
    assert(!info.cuda_available);
    assert(info.build_mode == "CPU_ONLY");
    std::cout << "  ✓ CPU-Only mode correctly reported without fabrication\n";
#endif

    // Verification 6: Summary string stream generation
    std::ostringstream oss;
    titan::HardwareProbe::print_summary(oss);
    assert(!oss.str().empty());
    assert(oss.str().find("NEXUS TITAN") != std::string::npos);
    std::cout << "  ✓ Diagnostic summary generated successfully\n";

    // Print summary to console for audit trail
    std::cout << "\n" << oss.str() << "\n";
    std::cout << "[TEST PASSED] titan::HardwareProbe verification complete.\n";
    return 0;
}
