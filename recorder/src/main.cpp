#include "include/shared_memory.h"
#include "include/database.h"
#include "include/race_session.h"
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    std::cout << "AMS2 Race Recorder" << std::endl;
    std::cout << "==================" << std::endl;
    
    // Initialize database
    Database db("ams2_races.db");
    if (!db.Initialize()) {
        std::cerr << "Failed to initialize database." << std::endl;
        return 1;
    }
    
    // Initialize shared memory reader
    SharedMemoryReader smReader;
    if (!smReader.Initialize()) {
        std::cerr << "Failed to connect to AMS2 shared memory." << std::endl;
        std::cerr << "Make sure Automobilista 2 is running and shared memory is enabled." << std::endl;
        return 1;
    }
    
    // Initialize race session handler
    RaceSession session(db);
    
    std::cout << "Connected to AMS2. Waiting for race data..." << std::endl;
    
    // Main loop
    bool running = true;
    SharedMemory data;
    std::string lastTrackName;
    std::string lastCarName;
    SessionState lastSessionState = SessionState::SESSION_INVALID;
    
    while (running) {
        if (smReader.ReadData(data)) {
            // Check if session started
            SessionState currentState = static_cast<SessionState>(data.mSessionState);
            
            if (currentState != lastSessionState && 
                (currentState == SessionState::SESSION_QUALIFY || 
                 currentState == SessionState::SESSION_RACE)) {
                
                // Start new session
                std::string sessionType = (currentState == SessionState::SESSION_QUALIFY) 
                    ? "Qualifying" : "Race";
                std::string trackName = "Unknown Track";  // Would extract from data
                std::string carName = "Unknown Car";      // Would extract from data
                
                session.StartSession(sessionType, trackName, carName);
            }
            
            // Process frame
            session.ProcessFrame(data);
            
            lastSessionState = currentState;
        } else {
            std::cerr << "Failed to read shared memory." << std::endl;
        }
        
        // Sleep to avoid busy-waiting (update ~60 times per second)
        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }
    
    // Cleanup
    if (session.IsSessionActive()) {
        session.EndSession();
    }
    
    db.Close();
    smReader.Disconnect();
    
    std::cout << "AMS2 Race Recorder stopped." << std::endl;
    return 0;
}
