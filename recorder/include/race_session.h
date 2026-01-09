#pragma once

#include "shared_memory.h"
#include "database.h"
#include <vector>
#include <map>
#include <string>

class RaceSession {
public:
    RaceSession(Database& db);
    
    // Session lifecycle
    void ProcessFrame(const SharedMemory& data);
    void StartSession(const std::string& sessionType, const std::string& trackName, 
                     const std::string& carName);
    void EndSession();
    
    // State queries
    bool IsSessionActive() const;
    SessionState GetCurrentSessionState() const;
    
private:
    Database& mDb;
    int mCurrentSessionId;
    SessionState mLastSessionState;
    std::map<std::string, RaceResult> mParticipantResults;
    
    struct SessionData {
        bool poleSitterRecorded = false;
        std::string poleSitter;
        std::map<std::string, float> bestLapTimes;  // For fastest lap detection
        std::map<std::string, int> participantIndices;
    } mSessionData;
    
    // Helper methods
    void ProcessQualifySession(const SharedMemory& data);
    void ProcessRaceSession(const SharedMemory& data);
    void RecordPoleSitter(const SharedMemory& data);
    void RecordFastestLap(const SharedMemory& data);
    void UpdateParticipantData(const SharedMemory& data);
    void CalculateF1Points(int position);
    
    // F1 2024 points table
    static constexpr int F1_POINTS_TABLE[] = {
        25, 18, 15, 12, 10, 8, 6, 4, 2, 1  // Top 10
    };
};
