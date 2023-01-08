const Queries =  {
    TELEOP_UPPER_HUB: "teleop_upper_hub",
    AUTO_UPPER_HUB: "auto_upper_hub",
    TELEOP_LOWER_HUB: "teleop_lower_hub",
    AUTO_LOWER_HUB: "auto_lower_hub",
    TELEOP_MISSES: "teleop_misses",
    AUTO_MISSES: "auto_misses",
    DRIVER_RATING: "driver_rating",
    DEFENSE_RATING: "defense_rating",
    COUNTER_DEFENSE_RATING: "counter_defense_rating",
    TELEOP_TOTAL: {
        "teleop_upper_hub": 1, 
        "teleop_lower_hub": 2
    },
    AUTO_TOTAL: {
        "auto_lower_hub": 2, 
        "auto_upper_hub": 4
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
    TEAMS: [33, 2056, 4499, 2468, 4099, 118, 180, 340, 5406],
    RED: "red",
    BLUE: "blue"
}

const mandatoryMatchData = {
    MATCH_KEY: "match_key",
    ALLIANCE: "alliance",
    TEAM_NUMBER: "team_number"
}

const JSONData = "https://raw.githubusercontent.com/team4099/FalconScout/main/falconscoutcore/data/2022iri_match_data.json"

export { Queries, Selections, JSONData, mandatoryMatchData }