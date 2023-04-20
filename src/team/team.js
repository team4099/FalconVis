import { CalculatedStats } from '../lib/data/CalculatedStats.js';
import { Queries, JSONData, Selections, mandatoryMatchData } from '../lib/data/Constants.js'
import { Factor } from '../lib/automated/Factor.js'
import { BarGraph } from '../lib/components/BarGraph.js'
import { GraphManager } from '../lib/components/GraphManager.js';
import { Modal } from '../lib/components/Modal.js';
import { AutomatedMacro } from '../lib/components/AutomatedMacro.js';
import { CompositeStat } from '../lib/automated/CompositeStat.js'
import { setTeams, setupTeams, statManager } from './teamParent.js'
import { LineGraph } from '../lib/components/LineGraph.js';
import { HeatMap } from '../lib/components/HeatMap.js';
import { NoteHighlighting } from '../lib/components/NoteHighlighting.js';
import { StackedBarGraph } from '../lib/components/StackedBarGraph.js';

(async () => {
    console.log("test")
    var data = await fetch(JSONData).then(res => res.json())
    var stats = new CalculatedStats(data)
    var modal = new Modal("editModal", "fakeToggle", "getEditedData", "editableFormContainer")
    console.log(stats.data)

    var team = [Selections.TEAMS[0]]
    
    statManager.addGraph(
        "avr_points_contributed",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. Points Contributed", 
            new CompositeStat(
                [new Factor(function (team) { 
                    let pointsAdded = stats.getPointsAddedByMatch(team, true)
                    return pointsAdded.reduce((a, b) => a + b) / pointsAdded.length
                })],
                30.0
            ),
            team
        )
    )

    statManager.addGraph(
        "avr_teleop_cycles",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. Teleop Cycles Count", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrStat(team,mandatoryMatchData.TELEOP_GRID)})],
                5
            ),
            team
        )
    )

    statManager.addGraph(
        "avr_auto_cycles",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. auto cycle count", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrStat(team,mandatoryMatchData.AUTO_GRID)})],
                1.5
            ),
            team
        )
    )

    statManager.addGraph(
        "avr_mobility (pcnt)",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. Mobility", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getScoreDataCritSingle(team, Queries.MOBILITY, Queries.MOBILITY_CRIT)})],
                50.00
            ),
            team
        )
    )  

    statManager.addGraph(
        "auto_engage_attempts",
        new AutomatedMacro(
            "macrosContainer", 
            "Auto Engage Attempts", 
            new CompositeStat(
                [new Factor(function (team) { 
                    return stats.getScoreDataCrit(team, Queries.AUTO_ATTEMPTED_CHARGING_STATE, Queries.ENGAGE_CRIT)[1].reduce(
                        (a, b) => a + b
                    )
                })],
                6
            ),
            team
        )
    )

    statManager.addGraph(
        "auto_engage_accuracy (pcnt)",
        new AutomatedMacro(
            "macrosContainer", 
            "Auto Engage Accuracy", 
            new CompositeStat(
                [new Factor(function (team) { 
                    let accuracy = stats.getScoreDataCritSingle(team, Queries.AUTO_CHARGING_STATE, Queries.ENGAGE_CRIT) / stats.getScoreDataCritSingle(team, Queries.AUTO_ATTEMPTED_CHARGING_STATE, Queries.ENGAGE_CRIT)
                    return accuracy * 100
                })],
                75.00
            ),
            team
        )
    )

    statManager.addGraph(
        "avr_auto_accuracy",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. Auto Accuracy (Pcnt)", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrGridMissed(team, Queries.AUTONOMOUS)})],
                80
            ),
            team
        )
    )

    statManager.addGraph(
        "avr_teleop_accuracy",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. Teleop Accuracy (Pcnt)", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrGridMissed(team,Queries.TELEOP)})],
                80
            ),
            team
        )
    )

    statManager.addGraph(
        "avr_driver_rating",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. Driver Rating", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrStat(team,Queries.DRIVER_RATING)})],
                60
            ),
            team
        )
    )
    

    statManager.addGraph(
        "heightsScoreGraph",
        new BarGraph(
            "graphContainer",
            "Score by heights (any piece)",
            {
                bar: {
                    horizon: false
                }
            },
            {
                formula: {
                    "High Avr": function(team) { return stats.getAvrTier(team, Queries.HIGH, Queries.TELEOP_GRID)},
                    "Mid Avr": function(team) { return stats.getAvrTier(team, Queries.MID, Queries.TELEOP_GRID)},
                    "Hybrid Avr": function(team) { return stats.getAvrTier(team, Queries.HYBRID, Queries.TELEOP_GRID)}
                },
                selectedOptions: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )

    statManager.addGraph(
        "driverStatsGraph",
        new BarGraph(
            "graphContainer",
            "Driver Stats",
            {
                bar: {
                    horizon: false
                }
            },
            {
                formula: {
                    "Drvr Rating": function(team) { return stats.getAvrStat(team, Queries.DRIVER_RATING)},
                    "Dfns Rating": function(team) { return stats.getAvrStat(team, Queries.DEFENSE_RATING)},
                    "Dfns Time": function(team) { return stats.getAvrStat(team, Queries.DEFENSE_TIME)},
                    "Cntr Dfns Rating": function(team) { return stats.getAvrStat(team, Queries.COUNTER_DEFENSE_RATING)},
                    "Cntr Dfns Time": function(team) { return stats.getAvrStat(team, Queries.COUNTER_DEFENSE_TIME)}
                },
                selectedOptions: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )
    
    statManager.addGraph(
        "auto charge station score over time",
        new LineGraph(
            "graphContainer",
            "Auto Charge Station POT",
            {},
            {
                formula: function(team) { 
                    return stats.getScoreDataCrit(team, Queries.AUTO_CHARGING_STATE, Queries.AUTO_CHARGE_STATION_CRIT)
                },
                selectedOptions: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )

    statManager.addGraph(
        "endgame score over time",
        new LineGraph(
            "graphContainer",
            "Endgame Score Over time",
            {},
            {
                formula: function(team) { return stats.getScoreDataCrit(team, Queries.TOTAL_ENDGAME, Queries.ENDGAME_CRIT)},
                selectedOptions: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )

    statManager.addGraph(
        "auto grid score over time",
        new LineGraph(
            "graphContainer",
            "Auto POT",
            {},
            {
                formula: function(team) { return stats.getAvrGridScore(team, Queries.AUTONOMOUS)},
                selectedOptions: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )

    statManager.addGraph(
        "teleop grid score over time",
        new LineGraph(
            "graphContainer",
            "Teleop POT",
            {},
            {
                formula: function(team) { return stats.getAvrGridScore(team, Queries.TELEOP)},
                selectedOptions: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )
    
    statManager.addGraph(
        "breakdown of GAME PIECES over time",
        new StackedBarGraph(
            "graphContainer",
            "Breakdown of Game Pieces Scored",
            {},
            {
                formula: function(team) { 
                    let autoGamePieces = stats.getTypeOfGamePiece(team, Queries.AUTO_GRID)
                    let teleopGamePieces = stats.getTypeOfGamePiece(team, Queries.TELEOP_GRID)
                    return autoGamePieces.map((value, index) => value + teleopGamePieces[index])
                },
                selectedOptions: team,
                allOptions: Selections.TEAMS,
                fields: ["Cones", "Cubes"],
                colors: ["#FACC15", "#7C3AED"]
            },
            modal,
            false,
            false,
            true
        )
    )
    
    statManager.addGraph(
        "teleop CYCLES over time",
        new LineGraph(
            "graphContainer",
            "Teleop CYCLES over time",
            {},
            {
                formula: function(team) { return stats.getAvrStatOverTime(team, Queries.TELEOP_GRID)},
                selectedOptions: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )

    statManager.addGraph(
        "auto CYCLES over time",
        new LineGraph(
            "graphContainer",
            "Auto CYCLES over time",
            {},
            {
                formula: function(team) { return stats.getAvrStatOverTime(team, Queries.AUTO_GRID)},
                selectedOptions: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )


    statManager.addGraph(
        "gridScoreGraph",
        new BarGraph(
            "graphContainer",
            "Score by grid (any piece)",
            {
                bar: {
                    horizon: false
                }
            },
            {
                formula: {
                    "Left grid": function(team) { return stats.getAvrGrid(team, Queries.LEFT, Queries.TELEOP_GRID)},
                    "Coop grid": function(team) { return stats.getAvrGrid(team, Queries.COOP, Queries.TELEOP_GRID)},
                    "Right grid": function(team) { return stats.getAvrGrid(team, Queries.RIGHT, Queries.TELEOP_GRID)}
                },
                selectedOptions: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )

    statManager.addGraph(
        "Teleop CYCLES heatmap",
        new HeatMap(
            "graphContainer",
            "Teleop CYCLES Heatmap",
            {},
            {
                formula: function(team) { return stats.getCycleHeatmapData(team, Queries.TELEOP_GRID) },
                selectedOption: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )
    
    statManager.addGraph(
        "Auto CYCLES heatmap",
        new HeatMap(
            "graphContainer",
            "Auto CYCLES Heatmap",
            {},
            {
                formula: function(team) { return stats.getCycleHeatmapData(team, Queries.AUTO_GRID) },
                selectedOption: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )

    statManager.addGraph(
    "TeleopNotes",
    new NoteHighlighting(
            "graphContainer",
            function (team) {return stats.getNotes(team, Queries.TELEOP_NOTES)},
            team,
            "Teleop Notes",
            ["cycle", "good", "fast", "score"],
            ["can't", "disable", "foul", "bad", "drop", "stuck", "poor", "missed", "slow", "only", "tippy"]
        )
    )

    setupTeams(Selections.TEAMS, "teams")
    setTeams(statManager, "teams")
    document.getElementById("teams").addEventListener("change", function () {setTeams(statManager, "teams")})

})()