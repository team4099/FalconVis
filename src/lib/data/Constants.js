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
    ENDGAME_CRIT: {
        "None": 0,  //TODO: Edit scores
        "Docked": 2,
        "Engaged": 7
    },
    TOTAL_ENDGAME: "EndgameFinalCharge",
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
    MOBILITY: "Mobile",
    MOBILITY_CRIT: {
        "true": 100,
        "false": 0
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
    TEAMS: [1111, 1123, 1389, 1446, 1731, 1895, 1908, 2199, 
        2377, 2534, 2537, 2900, 2914, 2961, 4099, 4456, 449, 
        4638, 4821, 5338, 5549, 5587, 5830, 5841, 611, 614, 
        620, 6239, 6326, 6863, 7886, 8326, 836, 8514, 8622, 888],
        /*
        116, 339, 612, 620, 623, 686, 1389, 1418, 
        1719, 1727, 1885, 1915, 2186, 2421, 2849, 2961, 2988, 
        3361, 3373, 3748, 3793, 4099, 4472, 4541, 4638, 5115, 
        5243, 5587, 5841, 6504, 6882, 7770, 8197, 8230, 8590, 8592,
        8726, 9033, 9072, 9235
        */
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

const JSONData = "https://raw.githubusercontent.com/team4099/ScoutingAppData/main/2023mdbet_match_data.json"

export { Queries, Selections, JSONData, mandatoryMatchData }