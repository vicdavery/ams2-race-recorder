#include "../include/shared_memory.h"
#include <iostream>
#include <cstring>

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#endif

SharedMemoryReader::SharedMemoryReader()
    : mHandle(nullptr), mConnected(false) {
}

SharedMemoryReader::~SharedMemoryReader() {
    Disconnect();
}

bool SharedMemoryReader::Initialize() {
    return ConnectToSharedMemory();
}

bool SharedMemoryReader::ConnectToSharedMemory() {
#ifdef _WIN32
    // Windows shared memory implementation
    HANDLE hMapFile = OpenFileMappingA(
        FILE_MAP_READ,
        FALSE,
        "Local\\$pcars2$"  // AMS2 uses the same shared memory name as PCARS2
    );
    
    if (hMapFile == NULL) {
        std::cerr << "Failed to open shared memory: " << GetLastError() << std::endl;
        return false;
    }
    
    mHandle = hMapFile;
    mConnected = true;
    std::cout << "Connected to AMS2 shared memory." << std::endl;
    return true;
#else
    // Linux shared memory implementation
    // AMS2 is Windows-only, but providing fallback for development
    std::cerr << "Shared memory access requires Windows." << std::endl;
    return false;
#endif
}

bool SharedMemoryReader::ReadData(SharedMemory& data) {
    if (!mConnected || !mHandle) {
        std::cerr << "Not connected to shared memory." << std::endl;
        return false;
    }

#ifdef _WIN32
    LPVOID pBuf = MapViewOfFile(
        (HANDLE)mHandle,
        FILE_MAP_READ,
        0, 0,
        sizeof(SharedMemory)
    );
    
    if (pBuf == NULL) {
        std::cerr << "Failed to map view of file: " << GetLastError() << std::endl;
        return false;
    }
    
    // Copy data from shared memory
    std::memcpy(&data, pBuf, sizeof(SharedMemory));
    
    // Unmap the view
    UnmapViewOfFile(pBuf);
    
    return true;
#else
    return false;
#endif
}

bool SharedMemoryReader::IsConnected() const {
    return mConnected;
}

void SharedMemoryReader::Disconnect() {
    if (mHandle) {
#ifdef _WIN32
        CloseHandle((HANDLE)mHandle);
#endif
        mHandle = nullptr;
    }
    mConnected = false;
}
