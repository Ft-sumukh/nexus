#include "titan/hardware_probe.hpp"

#include <thread>
#include <iomanip>
#include <vector>

#if defined(_WIN32)
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
#elif defined(__linux__) || defined(__APPLE__)
#include <unistd.h>
#include <sys/types.h>
#include <sys/param.h>
#if defined(__APPLE__)
#include <sys/sysctl.h>
#endif
#endif

#if defined(TITAN_CUDA_ENABLED)
#include <cuda_runtime.h>
#endif

namespace titan {

HardwareInfo HardwareProbe::probe() {
    HardwareInfo info;

    // Logical core detection via C++ standard library fallback
    info.logical_cores = std::thread::hardware_concurrency();

#if defined(_WIN32)
    // CPU Architecture & Detailed OS info on Windows
    SYSTEM_INFO sysInfo;
    GetNativeSystemInfo(&sysInfo);

    switch (sysInfo.wProcessorArchitecture) {
        case PROCESSOR_ARCHITECTURE_AMD64:
            info.cpu_architecture = "x86_64 (AMD64)";
            break;
        case PROCESSOR_ARCHITECTURE_ARM64:
            info.cpu_architecture = "ARM64";
            break;
        case PROCESSOR_ARCHITECTURE_INTEL:
            info.cpu_architecture = "x86 (32-bit)";
            break;
        default:
            info.cpu_architecture = "Unknown Architecture";
            break;
    }

    // Physical core detection on Windows
    DWORD length = 0;
    GetLogicalProcessorInformation(nullptr, &length);
    if (GetLastError() == ERROR_INSUFFICIENT_BUFFER && length > 0) {
        std::vector<SYSTEM_LOGICAL_PROCESSOR_INFORMATION> buffer(length / sizeof(SYSTEM_LOGICAL_PROCESSOR_INFORMATION));
        if (GetLogicalProcessorInformation(buffer.data(), &length)) {
            unsigned int physical = 0;
            for (const auto& item : buffer) {
                if (item.Relationship == RelationProcessorCore) {
                    physical++;
                }
            }
            if (physical > 0) {
                info.physical_cores = physical;
            }
        }
    }
    if (info.physical_cores == 0) {
        info.physical_cores = info.logical_cores > 0 ? (info.logical_cores / 2 > 0 ? info.logical_cores / 2 : 1) : 1;
    }

    // RAM detection on Windows
    MEMORYSTATUSEX memStatus;
    memStatus.dwLength = sizeof(memStatus);
    if (GlobalMemoryStatusEx(&memStatus)) {
        info.total_physical_memory_bytes = memStatus.ullTotalPhys;
        info.available_physical_memory_bytes = memStatus.ullAvailPhys;
    }

#elif defined(__linux__)
    info.cpu_architecture = "Linux";
    long pages = sysconf(_SC_PHYS_PAGES);
    long page_size = sysconf(_SC_PAGE_SIZE);
    if (pages > 0 && page_size > 0) {
        info.total_physical_memory_bytes = static_cast<uint64_t>(pages) * static_cast<uint64_t>(page_size);
    }
    long avail_pages = sysconf(_SC_AVPHYS_PAGES);
    if (avail_pages > 0 && page_size > 0) {
        info.available_physical_memory_bytes = static_cast<uint64_t>(avail_pages) * static_cast<uint64_t>(page_size);
    }
    info.physical_cores = info.logical_cores > 1 ? info.logical_cores / 2 : 1;
#elif defined(__APPLE__)
    info.cpu_architecture = "Apple Silicon / macOS";
    int mib[2] = {CTL_HW, HW_MEMSIZE};
    uint64_t mem = 0;
    size_t len = sizeof(mem);
    if (sysctl(mib, 2, &mem, &len, nullptr, 0) == 0) {
        info.total_physical_memory_bytes = mem;
    }
    info.physical_cores = info.logical_cores > 1 ? info.logical_cores / 2 : 1;
#endif

    // Accelerator / CUDA detection
#if defined(TITAN_CUDA_ENABLED)
    int deviceCount = 0;
    cudaError_t err = cudaGetDeviceCount(&deviceCount);
    if (err == cudaSuccess && deviceCount > 0) {
        info.cuda_available = true;
        info.gpu_device_count = deviceCount;
        cudaDeviceProp prop;
        if (cudaGetDeviceProperties(&prop, 0) == cudaSuccess) {
            info.gpu_device_name = prop.name;
        }
        info.build_mode = "CUDA_ENABLED";
    } else {
        info.cuda_available = false;
        info.gpu_device_name = "None (CUDA runtime error or no GPU)";
        info.gpu_device_count = 0;
        info.build_mode = "CUDA_BUILD_NO_DEVICE";
    }
#else
    info.cuda_available = false;
    info.gpu_device_name = "None (Compiled in CPU-Only Mode)";
    info.gpu_device_count = 0;
    info.build_mode = "CPU_ONLY";
#endif

    return info;
}

void HardwareProbe::print_summary(std::ostream& os) {
    const auto info = probe();
    const double total_gb = static_cast<double>(info.total_physical_memory_bytes) / (1024.0 * 1024.0 * 1024.0);
    const double avail_gb = static_cast<double>(info.available_physical_memory_bytes) / (1024.0 * 1024.0 * 1024.0);

    os << "========================================================\n"
       << "  NEXUS TITAN — Host Hardware Diagnostics\n"
       << "========================================================\n"
       << "  CPU Architecture:  " << info.cpu_architecture << "\n"
       << "  Physical Cores:    " << info.physical_cores << "\n"
       << "  Logical Threads:   " << info.logical_cores << "\n"
       << "  Total Memory:      " << std::fixed << std::setprecision(2) << total_gb << " GB\n"
       << "  Available Memory:  " << std::fixed << std::setprecision(2) << avail_gb << " GB\n"
       << "  Build Mode:        " << info.build_mode << "\n"
       << "  CUDA Available:    " << (info.cuda_available ? "YES" : "NO (CPU Fallback Active)") << "\n"
       << "  GPU Device:        " << info.gpu_device_name << "\n"
       << "========================================================\n";
}

} // namespace titan
