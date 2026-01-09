#include "../include/database.h"
#include <iostream>
#include <chrono>
#include <iomanip>
#include <sstream>

Database::Database(const std::string& dbPath)
    : mDb(nullptr), mDbPath(dbPath), mConnected(false) {
}

Database::~Database() {
    Close();
}

bool Database::Initialize() {
    int rc = sqlite3_open(mDbPath.c_str(), &mDb);
    
    if (rc != SQLITE_OK) {
        std::cerr << "Cannot open database: " << sqlite3_errmsg(mDb) << std::endl;
        return false;
    }
    
    mConnected = true;
    std::cout << "Opened database: " << mDbPath << std::endl;
    
    return CreateTables();
}

bool Database::IsConnected() const {
    return mConnected && mDb != nullptr;
}

bool Database::CreateTables() {
    const char* sql =
        "CREATE TABLE IF NOT EXISTS sessions ("
        "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  session_type TEXT NOT NULL,"
        "  track_name TEXT NOT NULL,"
        "  car_name TEXT NOT NULL,"
        "  date_time TEXT NOT NULL"
        ");"
        "CREATE TABLE IF NOT EXISTS results ("
        "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  session_id INTEGER NOT NULL,"
        "  driver_name TEXT NOT NULL,"
        "  finish_position INTEGER NOT NULL,"
        "  points INTEGER NOT NULL DEFAULT 0,"
        "  fastest_lap BOOLEAN DEFAULT 0,"
        "  pole_sitter BOOLEAN DEFAULT 0,"
        "  session_best_lap REAL,"
        "  race_best_lap REAL,"
        "  laps_completed INTEGER,"
        "  FOREIGN KEY(session_id) REFERENCES sessions(id)"
        ");";
    
    char* errMsg = nullptr;
    int rc = sqlite3_exec(mDb, sql, 0, 0, &errMsg);
    
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << errMsg << std::endl;
        sqlite3_free(errMsg);
        return false;
    }
    
    std::cout << "Database tables created/verified." << std::endl;
    return true;
}

int Database::CreateSession(const std::string& sessionType, const std::string& trackName,
                           const std::string& carName) {
    std::string dateTime = GetCurrentDateTime();
    
    const char* sql = "INSERT INTO sessions (session_type, track_name, car_name, date_time) VALUES (?, ?, ?, ?);";
    
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(mDb, sql, -1, &stmt, nullptr);
    
    if (rc != SQLITE_OK) {
        std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(mDb) << std::endl;
        return -1;
    }
    
    sqlite3_bind_text(stmt, 1, sessionType.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, trackName.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, carName.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 4, dateTime.c_str(), -1, SQLITE_STATIC);
    
    rc = sqlite3_step(stmt);
    sqlite3_finalize(stmt);
    
    if (rc != SQLITE_DONE) {
        std::cerr << "Failed to insert session: " << sqlite3_errmsg(mDb) << std::endl;
        return -1;
    }
    
    int sessionId = static_cast<int>(sqlite3_last_insert_rowid(mDb));
    std::cout << "Created session ID: " << sessionId << std::endl;
    return sessionId;
}

bool Database::SaveSessionResults(int sessionId, const std::vector<RaceResult>& results) {
    const char* sql = 
        "INSERT INTO results (session_id, driver_name, finish_position, points, "
        "fastest_lap, pole_sitter, session_best_lap, race_best_lap, laps_completed) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);";
    
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(mDb, sql, -1, &stmt, nullptr);
    
    if (rc != SQLITE_OK) {
        std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(mDb) << std::endl;
        return false;
    }
    
    for (const auto& result : results) {
        sqlite3_bind_int(stmt, 1, sessionId);
        sqlite3_bind_text(stmt, 2, result.driverName.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_int(stmt, 3, result.finishPosition);
        sqlite3_bind_int(stmt, 4, result.points);
        sqlite3_bind_int(stmt, 5, result.fastestLap ? 1 : 0);
        sqlite3_bind_int(stmt, 6, result.poleSitter ? 1 : 0);
        sqlite3_bind_double(stmt, 7, result.sessionBestLap);
        sqlite3_bind_double(stmt, 8, result.raceBestLap);
        sqlite3_bind_int(stmt, 9, result.lapsCompleted);
        
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << "Failed to insert result: " << sqlite3_errmsg(mDb) << std::endl;
            sqlite3_finalize(stmt);
            return false;
        }
        
        sqlite3_reset(stmt);
    }
    
    sqlite3_finalize(stmt);
    std::cout << "Saved " << results.size() << " results for session " << sessionId << std::endl;
    return true;
}

std::vector<SessionRecord> Database::GetSessions(int limit) {
    std::vector<SessionRecord> sessions;
    
    const char* sql = "SELECT id, session_type, track_name, car_name, date_time FROM sessions ORDER BY id DESC LIMIT ?;";
    
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(mDb, sql, -1, &stmt, nullptr);
    
    if (rc != SQLITE_OK) {
        std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(mDb) << std::endl;
        return sessions;
    }
    
    sqlite3_bind_int(stmt, 1, limit);
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        SessionRecord record;
        record.sessionId = sqlite3_column_int(stmt, 0);
        record.sessionType = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        record.trackName = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        record.carName = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
        record.dateTime = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
        
        sessions.push_back(record);
    }
    
    sqlite3_finalize(stmt);
    return sessions;
}

SessionRecord Database::GetSessionById(int sessionId) {
    SessionRecord record;
    
    const char* sql = "SELECT id, session_type, track_name, car_name, date_time FROM sessions WHERE id = ?;";
    
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(mDb, sql, -1, &stmt, nullptr);
    
    if (rc != SQLITE_OK) {
        std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(mDb) << std::endl;
        return record;
    }
    
    sqlite3_bind_int(stmt, 1, sessionId);
    
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        record.sessionId = sqlite3_column_int(stmt, 0);
        record.sessionType = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        record.trackName = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        record.carName = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
        record.dateTime = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
    }
    
    sqlite3_finalize(stmt);
    return record;
}

std::string Database::GetCurrentDateTime() {
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S");
    return ss.str();
}

void Database::Close() {
    if (mDb) {
        sqlite3_close(mDb);
        mDb = nullptr;
    }
    mConnected = false;
}
