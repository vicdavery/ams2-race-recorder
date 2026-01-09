#pragma once

#include <cstdint>
#include <array>
#include <string>

// Constants from AMS2 shared memory definition
constexpr int SHARED_MEMORY_VERSION = 13;
constexpr int STRING_LENGTH_MAX = 64;
constexpr int STORED_PARTICIPANTS_MAX = 64;
constexpr int TYRE_COMPOUND_NAME_LENGTH_MAX = 40;

// Enum values
enum class GameState : uint32_t {
    GAME_EXITED = 0,
    GAME_FRONT_END = 1,
    GAME_INGAME_PLAYING = 2,
    GAME_INGAME_PAUSED = 3,
    GAME_INGAME_INMENU_TIME_TICKING = 4,
    GAME_INGAME_RESTARTING = 5,
    GAME_INGAME_REPLAY = 6,
    GAME_FRONT_END_REPLAY = 7
};

enum class SessionState : uint32_t {
    SESSION_INVALID = 0,
    SESSION_PRACTICE = 1,
    SESSION_TEST = 2,
    SESSION_QUALIFY = 3,
    SESSION_FORMATION_LAP = 4,
    SESSION_RACE = 5,
    SESSION_TIME_ATTACK = 6
};

enum class RaceState : uint32_t {
    RACE_STATE_INVALID = 0,
    RACE_STATE_NOT_STARTED = 1,
    RACE_STATE_RACING = 2,
    RACE_STATE_FINISHED = 3,
    RACE_STATE_DISQUALIFIED = 4,
    RACE_STATE_RETIRED = 5,
    RACE_STATE_DNF = 6
};

// Participant Info structure
struct ParticipantInfo {
    bool mIsActive;
    char mName[STRING_LENGTH_MAX];
    float mWorldPosition[3];
    float mOrientation[3];
    float mLocalVelocity[3];
    float mWorldVelocity[3];
    float mAngularVelocity[3];
    float mLocalAcceleration[3];
    float mWorldAcceleration[3];
    float mExtentsCentre[3];
    uint32_t mIsPlayer;
    uint32_t mFinishStatus;
    uint32_t mLapsCompleted;
    uint32_t mCurrentLapInvalid;
    float mLapTimeCurrentLapMs;
    float mSessionBestLapTime;
    float mPersonalBestLapTime;
    float mCurrentSector1TimeMs;
    float mCurrentSector2TimeMs;
    float mCurrentSector3TimeMs;
    float mSessionBestSector1TimeMs;
    float mSessionBestSector2TimeMs;
    float mSessionBestSector3TimeMs;
    float mPersonalBestSector1TimeMs;
    float mPersonalBestSector2TimeMs;
    float mPersonalBestSector3TimeMs;
    float mSectorStartTime;
    uint32_t mParticipantIndex;
    uint32_t mTireCompoundIndex;
    char mTireCompoundName[TYRE_COMPOUND_NAME_LENGTH_MAX];
    uint32_t mPitMode;
    uint32_t mPitSchedule;
    uint32_t mHighestFlagColour;
    uint32_t mUnlap;
    uint32_t mPitCount;
    uint32_t mPenaltyCount;
    float mIncarRating;
    float mAntiRollBarAdjustmentF;
    float mAntiRollBarAdjustmentR;
    uint32_t mBrakeTorque;
    uint32_t mBrakeBiasFront;
    float mTurboBoostPressure;
    uint32_t mCurrentGear;
    uint32_t mMaxGears;
    float mSteerInputRaw;
    float mSteerInputSmoothed;
    float mThrottleInputRaw;
    float mThrottleInputSmoothed;
    float mBrakeInputRaw;
    float mBrakeInputSmoothed;
    float mClutchInputRaw;
    float mClutchInputSmoothed;
    uint32_t mSPLapStatus;
    float mRadarRelativeVelocityToNextCar;
    float mRadarRelativeDistanceToNextCar;
};

// Main shared memory structure
struct SharedMemory {
    uint32_t mVersion;
    uint32_t mBuildVersionNumber;
    uint32_t mGameState;
    uint32_t mSessionState;
    uint32_t mRaceState;
    int32_t mViewedParticipantIndex;
    int32_t mNumParticipants;
    std::array<ParticipantInfo, STORED_PARTICIPANTS_MAX> mParticipantInfo;
    
    // Add more fields as needed - this is a simplified structure
};

class SharedMemoryReader {
public:
    SharedMemoryReader();
    ~SharedMemoryReader();
    
    bool Initialize();
    bool ReadData(SharedMemory& data);
    bool IsConnected() const;
    void Disconnect();
    
private:
    void* mHandle;
    bool mConnected;
    
    bool ConnectToSharedMemory();
};
