#pragma once

#include <sqlite3.h>
#include <string>
#include <vector>

struct RaceResult {
    std::string driverName;
    int finishPosition;
    int points;
    bool fastestLap;
    bool poleSitter;
    float sessionBestLap;
    float raceBestLap;
    int lapsCompleted;
};

struct SessionRecord {
    int sessionId;
    std::string sessionType;  // "practice", "qualify", "race"
    std::string trackName;
    std::string carName;
    std::string dateTime;
    std::vector<RaceResult> results;
};

class Database {
public:
    Database(const std::string& dbPath);
    ~Database();
    
    bool Initialize();
    bool IsConnected() const;
    
    // Session management
    int CreateSession(const std::string& sessionType, const std::string& trackName, 
                      const std::string& carName);
    bool SaveSessionResults(int sessionId, const std::vector<RaceResult>& results);
    
    // Queries
    std::vector<SessionRecord> GetSessions(int limit = 50);
    SessionRecord GetSessionById(int sessionId);
    
    // Utility
    void Close();
    
private:
    sqlite3* mDb;
    std::string mDbPath;
    bool mConnected;
    
    bool CreateTables();
    std::string GetCurrentDateTime();
};
