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
        "None": 0,  //TODO: Edit scores
        "Parked": 0,
        "Docked": 0,
        "Engage": 1
    },
    TOTAL_ENDGAME: "EndgameFinalCharge",
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
    MOBILITY_POINAGE: {
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
    TEAMS: [116, 122, 346, 384, 401, 422, 449, 611, 612, 614, 620, 623, 686, 836, 888, 977, 1086, 1111, 1123, 1262, 1389, 1418, 1599, 1610, 1629, 1727, 1731, 1895, 1908, 2028, 2068, 2106, 2199, 2363, 2377, 2421, 2537, 3136, 3373, 3939, 4099, 4456, 4472, 4541, 5115, 5338, 5549, 5587, 5724, 5804, 6326, 6802, 6863, 7770, 8230, 8592, 8622, 8726, 9033, 9072],
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

const JSONData = "https://raw.githubusercontent.com/team4099/ScoutingAppData/main/2023chcmp_match_data.json"

export { Queries, Selections, JSONData, mandatoryMatchData }