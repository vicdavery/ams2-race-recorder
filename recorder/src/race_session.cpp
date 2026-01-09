#include "../include/race_session.h"
#include <iostream>
#include <algorithm>

RaceSession::RaceSession(Database& db)
    : mDb(db), mCurrentSessionId(-1), mLastSessionState(SessionState::SESSION_INVALID) {
}

void RaceSession::ProcessFrame(const SharedMemory& data) {
    SessionState currentState = static_cast<SessionState>(data.mSessionState);
    
    // Detect session change
    if (currentState != mLastSessionState) {
        if (mLastSessionState != SessionState::SESSION_INVALID && IsSessionActive()) {
            EndSession();
        }
        mLastSessionState = currentState;
    }
    
    // Process based on session state
    if (currentState == SessionState::SESSION_QUALIFY) {
        ProcessQualifySession(data);
    } else if (currentState == SessionState::SESSION_RACE) {
        ProcessRaceSession(data);
    }
    
    // Update participant data continuously
    UpdateParticipantData(data);
}

void RaceSession::StartSession(const std::string& sessionType, const std::string& trackName,
                              const std::string& carName) {
    if (mCurrentSessionId != -1) {
        EndSession();
    }
    
    mCurrentSessionId = mDb.CreateSession(sessionType, trackName, carName);
    mSessionData = {};
    mParticipantResults.clear();
    
    std::cout << "Session started: " << sessionType << " at " << trackName << std::endl;
}

void RaceSession::EndSession() {
    if (mCurrentSessionId == -1) {
        return;
    }
    
    // Convert results map to vector
    std::vector<RaceResult> results;
    for (auto& pair : mParticipantResults) {
        results.push_back(pair.second);
    }
    
    // Sort by position
    std::sort(results.begin(), results.end(),
        [](const RaceResult& a, const RaceResult& b) {
            return a.finishPosition < b.finishPosition;
        });
    
    // Save to database
    if (mDb.SaveSessionResults(mCurrentSessionId, results)) {
        std::cout << "Session " << mCurrentSessionId << " ended and saved." << std::endl;
    }
    
    mCurrentSessionId = -1;
    mParticipantResults.clear();
    mSessionData = {};
}

bool RaceSession::IsSessionActive() const {
    return mCurrentSessionId != -1;
}

SessionState RaceSession::GetCurrentSessionState() const {
    return mLastSessionState;
}

void RaceSession::ProcessQualifySession(const SharedMemory& data) {
    // Record pole sitter once at the start of qualifying
    if (!mSessionData.poleSitterRecorded && data.mNumParticipants > 0) {
        RecordPoleSitter(data);
        mSessionData.poleSitterRecorded = true;
    }
    
    // Track fastest laps during qualifying
    RecordFastestLap(data);
}

void RaceSession::ProcessRaceSession(const SharedMemory& data) {
    // Track fastest laps during race
    RecordFastestLap(data);
}

void RaceSession::RecordPoleSitter(const SharedMemory& data) {
    float bestLapTime = 999999.0f;
    std::string poleSitter;
    
    for (int i = 0; i < data.mNumParticipants; ++i) {
        const auto& participant = data.mParticipantInfo[i];
        
        if (!participant.mIsActive) continue;
        
        float lapTime = participant.mSessionBestLapTime;
        if (lapTime > 0 && lapTime < bestLapTime) {
            bestLapTime = lapTime;
            poleSitter = participant.mName;
        }
    }
    
    if (!poleSitter.empty()) {
        mSessionData.poleSitter = poleSitter;
        std::cout << "Pole sitter: " << poleSitter << " (" << bestLapTime << "ms)" << std::endl;
        
        if (mParticipantResults.find(poleSitter) != mParticipantResults.end()) {
            mParticipantResults[poleSitter].poleSitter = true;
        }
    }
}

void RaceSession::RecordFastestLap(const SharedMemory& data) {
    for (int i = 0; i < data.mNumParticipants; ++i) {
        const auto& participant = data.mParticipantInfo[i];
        
        if (!participant.mIsActive) continue;
        
        std::string name = participant.mName;
        float currentBest = participant.mSessionBestLapTime;
        
        // Update best lap tracking
        if (currentBest > 0) {
            auto it = mSessionData.bestLapTimes.find(name);
            if (it == mSessionData.bestLapTimes.end()) {
                mSessionData.bestLapTimes[name] = currentBest;
            } else if (currentBest < it->second) {
                it->second = currentBest;
            }
        }
    }
}

void RaceSession::UpdateParticipantData(const SharedMemory& data) {
    for (int i = 0; i < data.mNumParticipants; ++i) {
        const auto& participant = data.mParticipantInfo[i];
        
        if (!participant.mIsActive) continue;
        
        std::string name = participant.mName;
        
        // Initialize if new participant
        if (mParticipantResults.find(name) == mParticipantResults.end()) {
            RaceResult result;
            result.driverName = name;
            result.finishPosition = participant.mLapsCompleted;
            result.points = 0;
            result.fastestLap = false;
            result.poleSitter = false;
            result.sessionBestLap = participant.mSessionBestLapTime;
            result.raceBestLap = participant.mPersonalBestLapTime;
            result.lapsCompleted = participant.mLapsCompleted;
            
            mParticipantResults[name] = result;
            mSessionData.participantIndices[name] = i;
        } else {
            // Update existing
            auto& result = mParticipantResults[name];
            result.sessionBestLap = participant.mSessionBestLapTime;
            result.raceBestLap = participant.mPersonalBestLapTime;
            result.lapsCompleted = participant.mLapsCompleted;
        }
    }
    
    // Determine fastest lap holder
    float bestLapTime = 999999.0f;
    std::string fastestLapDriver;
    
    for (const auto& pair : mSessionData.bestLapTimes) {
        if (pair.second < bestLapTime) {
            bestLapTime = pair.second;
            fastestLapDriver = pair.first;
        }
    }
    
    if (!fastestLapDriver.empty()) {
        for (auto& pair : mParticipantResults) {
            pair.second.fastestLap = (pair.first == fastestLapDriver);
        }
    }
}

// Note: This is simplified - actual F1 points assignment would be more complex
// This should be called based on final race standings
