const Queries =  {
    HIGH: "HIGH_TIER",
    MID: "MID_TIER",
    HYBRID: "HYBRID_TIER",
    LEFT: "LEFT_GRID",
    RIGHT: "RIGHT_GRID",
    COOP: "COOP_GRID",
    DEFENSE_RATING: "DefenseRating",
    DRIVER_RATING: "DriverRating",
    DEFENSE_TIME: "DefenseTime",
    COUNTER_DEFENSE_RATING: "CounterDefenseRating",
    COUNTER_DEFENSE_TIME: "DefendedTime",
    AUTO_CHARGE_STATION_CRIT: {
        "": 0,
        "None": 0,
        "Dock": 8,
        "Engage": 12
    },
    ENDGAME_CRIT: {
        "": 0,
        "None": 0,
        "Park": 2,
        "Dock": 6,
        "Engage": 10
    },
    ENGAGE_CRIT: {
        "": 0,
        "None": 0,
        "Park": 0,
        "Dock": 0,
        "Engage": 1
    },
    DOCKED_CRIT: {
        "": 0,
        "None": 0,
        "Park": 0,
        "Dock": 1,
        "Engage": 0
    },
    TOTAL_ENDGAME: "EndgameFinalCharge",
    AUTO_ATTEMPTED_CHARGING_STATE: "AutoAttemptedCharge",
    AUTO_CHARGING_STATE: "AutoChargingState",
    AUTO_TOTAL: {
        "auto_lower_hub": 2, 
        "auto_upper_hub": 4
    },
    AUTONOMOUS: "AUTONOMOUS",
    TELEOP: "TELEOP",
    AUTO_GRID: "AutoGrid",
    TELEOP_GRID: "TeleopGrid",
    AUTO_MISSES: "AutoMissed",
    TELEOP_MISSES: "TeleopMissed",
    AUTO_NOTES: "AutoNotes",
    TELEOP_NOTES: "TeleopNotes",
    ENDGAME_NOTES: "EndgameNotes",
    MOBILITY: "Mobile",
    DISABLED: "Disable",
    MOBILITY_CRIT: {
        1: 100,
        0: 0
    },
    MOBILITY_POINTAGE: {
        1: 3,
        0: 0
    },
    DISABLED_CRIT: {
        1: 1,
        0: 0
    },
    AUTO_GRID_SCORE: {
        "L": 3,
        "M": 4,
        "H": 6
    },
    TELEOP_GRID_SCORE: {
        "L": 2,
        "M": 3,
        "H": 5
    }
}

const Selections =  {
    MATCHES: [
        'qm1', 'qm2', 'qm3', 'qm4', 'qm5', 
        'qm6', 'qm7', 'qm8', 'qm9', 'qm10', 
        'qm11', 'qm12', 'qm13', 'qm14', 'qm15', 
        'qm16', 'qm17', 'qm18', 'qm19', 'qm20', 
        'qm21', 'qm22', 'qm23', 'qm24', 'qm25', 
        'qm26', 'qm27', 'qm28', 'qm29', 'qm30', 
        'qm31', 'qm32', 'qm33', 'qm34', 'qm35', 
        'qm36', 'qm37', 'qm38', 'qm39', 'qm40', 
        'qm41', 'qm42', 'qm43', 'qm44', 'qm45', 
        'qm46', 'qm47', 'qm48', 'qm49', 'qm50', 
        'qm51', 'qm52', 'qm53', 'qm54', 'qm55', 
        'qm56', 'qm57', 'qm58', 'qm59', 'qm60'
    ],
    TEAMS: [1023, 11, 1123, 1156, 1466, 1468, 1501, 1538, 1629, 1746, 1757, 177, 179, 1816, 1836, 195, 2642, 2960, 2992, 3003, 3039, 3161, 3184, 3218, 3478, 3538, 3572, 3767, 3932, 3940, 4069, 4099, 4112, 4143, 4145, 4329, 4419, 4522, 4663, 4905, 4909, 494, 4944, 5006, 503, 5135, 5172, 5274, 5338, 5553, 5665, 5804, 5990, 6431, 6606, 6657, 6817, 6909, 7072, 7285, 7428, 7617, 8015, 8016, 857, 8592, 8717, 8808, 8847, 900, 9023, 9030, 9062, 9084, 9126, 9140, 955],
    RED: "red",
    BLUE: "blue"
}

const mandatoryMatchData = {
    MATCH_KEY: "MatchKey",
    ALLIANCE: "Alliance",
    TEAM_NUMBER: "TeamNumber",
    AUTO_GRID: "AutoGrid",
    TELEOP_GRID: "TeleopGrid"
}

const JSONData = "https://raw.githubusercontent.com/team4099/FalconScout/2023falconscoutcore/falconscoutcore/data/2023new_match_data.json"

export { Queries, Selections, JSONData, mandatoryMatchData }