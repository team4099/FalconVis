import { Queries, Selections, JSONData, mandatoryMatchData } from '../lib/data/Constants.js'
import { BarGraph } from '../lib/components/BarGraph.js';
import { LineGraph } from '../lib/components/LineGraph.js';
import { BoxPlot } from '../lib/components/BoxPlot.js';
import { ScatterGraph } from '../lib/components/ScatterGraph.js';
import { PieGraph } from '../lib/components/PieGraph.js';
import { AutomatedMacro } from '../lib/components/AutomatedMacro.js';
import { WeightedStat } from '../lib/automated/WeightedStat.js'
import { CompositeStat } from '../lib/automated/CompositeStat.js'
import { Factor } from '../lib/automated/Factor.js'
import { CalculatedStats } from '../lib/data/CalculatedStats.js';
import { Modal } from "../lib/components/Modal.js"
import { GraphManager } from "../lib/components/GraphManager.js"
import { CombinedHeatmap } from "../lib/components/CombinedHeatmap.js"
import { 
    setTeams, modal, graphContainerBlue, 
    graphContainerRed, graphContainerComparison, red, blue 
} from './matchParent.js'
import { StackedBarGraph } from '../lib/components/StackedBarGraph.js';


(async () => {
    var data = await fetch(JSONData).then(res => res.json())
    var stats = new CalculatedStats(data)

    // Shared Stats and Properties here
    var defenseStat = new WeightedStat(
        [{
            formula: new Factor(function(team) {return stats.getAvrStat(team, Queries.DEFENSE_RATING)}),
            weight: 10
        },
        {
            formula: new Factor(function(team) {return stats.getAvrStat(team, Queries.DRIVER_RATING)}),
            weight: 10
        },
        {
            formula: new Factor(function(team) {return stats.getAvrStat(team, Queries.COUNTER_DEFENSE_RATING)}),
            weight: 10
        }],
        4
    )

    generateBlueGraphs()
    generateRedGraphs()
    generateComparisonGraphs()
    
    // Red Graphs Generated Here
    function generateRedGraphs() {
        let getOptimizedAuto = function() { 
            return stats.optimizeAuto(red)
        } // Lazy to avoid it reading only 9999 from the teams

        graphContainerRed.addGraph(
            "teleopCargoRed",
            new BarGraph(
                "redTeleopContainer",
                "Avr. Cycles - Red",
                {
                    bar: {
                        horizontal: false
                    }
                },
                {
                    formula: {
                    "Cycles": function(team) {return stats.getAvrStat(team, Queries.TELEOP_GRID)}
                    },
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        
        graphContainerRed.addGraph(
            "autoPOTRed",
            new LineGraph(
                "redAutoContainer",
                "Auto POT - Red",
                {},
                {
                    formula: function(team) {return stats.getAvrGridScore(team, Queries.AUTONOMOUS)},
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "autoChargeStationPOTRed",
            new LineGraph(
                "redAutoContainer",
                "Auto Charge Station POT - Red",
                {},
                {
                    formula: function(team) { 
                        return stats.getScoreDataCrit(team, Queries.AUTO_CHARGING_STATE, Queries.AUTO_CHARGE_STATION_CRIT)
                    },
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "autoEngageRed",
            new StackedBarGraph(
                "redAutoContainer",
                "Auto Engage Stats - Red",
                {},
                {
                    formula: function(team) { 
                        let successfulEngages = stats.getScoreDataCrit(team, Queries.AUTO_CHARGING_STATE, Queries.ENGAGE_CRIT)[1].reduce((a, b) => a + b)
                        let successfulDocks = stats.getScoreDataCrit(team, Queries.AUTO_CHARGING_STATE, Queries.DOCKED_CRIT)[1].reduce((a, b) => a + b)
                        let engageMissed = (
                            stats.getScoreDataCrit(team, Queries.AUTO_ATTEMPTED_CHARGING_STATE, Queries.ENGAGE_CRIT)[1].reduce((a, b) => a + b)
                            - successfulEngages
                            - successfulDocks
                        )
                        return [
                            successfulEngages,
                            successfulDocks,
                            engageMissed
                        ]

                    },
                    fields: ["# Of Successful Engages", "# of Docks", "# of Missed Engages"],
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "autoAccuracyRed",
            new StackedBarGraph(
                "redAutoContainer",
                "Auto Accuracy - Red",
                {},
                {
                    formula: function(team) { 
                        let totalAutoCycles = stats.getCumulativeStat(team, Queries.AUTO_GRID)
                        let totalAutoMisses = stats.getCumulativeStat(team, Queries.AUTO_MISSES)
                        return [
                            totalAutoCycles.reduce((a, b) => a + b),
                            totalAutoMisses.reduce((a, b) => a + b)
                        ]
                    },
                    fields: ["Total Auto Cycles", "Total Auto Misses"],
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        
        graphContainerRed.addGraph(
            "teleopPOTRed",
            new LineGraph(
                "redTeleopContainer",
                "Teleop POT - Red",
                {},
                {
                    formula: function(team) {return stats.getAvrGridScore(team, Queries.TELEOP)},
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "breakdown of POINTS ADDED",
            new StackedBarGraph(
                "redTeleopContainer",
                "Breakdown of Points Added by Team",
                {},
                {
                    formula: function(team) { 
                        let pointsAcrossAuto = stats.getPointsAddedByMatch(team, false, true)
                        let pointsAcrossTeleop = stats.getPointsAddedByMatch(team, false, false, true)
                        let totalPoints =  stats.getPointsAddedByMatch(team, true)

                        let averageAutoPoints = pointsAcrossAuto.reduce((a, b) => a + b) / pointsAcrossAuto.length
                        let averageTeleopPoints = pointsAcrossTeleop.reduce((a, b) => a + b) / pointsAcrossTeleop.length
                        let averageTotalPoints = totalPoints.reduce((a, b) => a + b) / totalPoints.length

                        let breakdownOfPointsAdded = [
                            averageAutoPoints.toFixed(2),
                            averageTeleopPoints.toFixed(2),
                            (averageTotalPoints - (averageAutoPoints + averageTeleopPoints)).toFixed(2)
                        ]

                        return breakdownOfPointsAdded
                    },
                    fields: ["Auto Contribution (pts.)", "Teleop Contribution (pts.)", "Endgame Contribution (pts.)"],
                    selectedOptions: red,
                    allOptions: Selections.TEAMS,
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "auto CYCLES over time",
            new LineGraph(
                "redAutoContainer",
                "Auto CYCLES over time - Red",
                {},
                {
                    formula: function(team) { return stats.getAvrStatOverTime(team, Queries.AUTO_GRID)},
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "teleop CYCLES over time",
            new LineGraph(
                "redTeleopContainer",
                "Teleop CYCLES over time - Red",
                {},
                {
                    formula: function(team) { return stats.getAvrStatOverTime(team, Queries.TELEOP_GRID)},
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "teleop CYCLES heatmap",
            new CombinedHeatmap(
                "redTeleopContainer",
                "Teleop CYCLES Heatmap (Combined) - Red",
                {},
                {
                    formula: function(team) { return stats.getCycleHeatmapData(team, Queries.TELEOP_GRID)},
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "auto CYCLES heatmap",
            new CombinedHeatmap(
                "redAutoContainer",
                "Auto CYCLES Heatmap (Combined) - Red",
                {},
                {
                    formula: function(team) { return stats.getCycleHeatmapData(team, Queries.AUTO_GRID)},
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )
        
        graphContainerRed.addGraph(
            "score for auto modes OPTIMIZED",
            new BarGraph(
                "redAutoContainer",
                "Best Possible Autonomous (pts.) - Red",
                {},
                {
                    formula: {
                        "Left Grid (pts.)": function(team) { 
                            let bestAutoConfig = getOptimizedAuto().filter(value => value[0] == team)[0]
                            return bestAutoConfig[1] == Queries.LEFT ? bestAutoConfig[2] : 0
                        },
                        "Co-Op Grid (pts.)": function(team) { 
                            let bestAutoConfig = getOptimizedAuto().filter(value => value[0] == team)[0]
                            return bestAutoConfig[1] == Queries.COOP ? bestAutoConfig[2] : 0
                        },
                        "Right Grid (pts.)": function(team) { 
                            let bestAutoConfig = getOptimizedAuto().filter(value => value[0] == team)[0]
                            return bestAutoConfig[1] == Queries.RIGHT ? bestAutoConfig[2] : 0
                        }
                    },
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "auto modes OPTIMIZED",
            new CombinedHeatmap(
                "redAutoContainer",
                "Best Configuration for Autonomous - Red",
                {},
                {
                    formula: function(team) { 
                        let bestAutoConfig = getOptimizedAuto().filter(value => value[0] == team)[0]
                        return stats.getCycleHeatmapData(team, Queries.AUTO_GRID, stats.data[team][bestAutoConfig[3]][mandatoryMatchData.MATCH_KEY]|| "qm0")
                    },
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )
    }

// Blue Graphs Generated Here
    function generateBlueGraphs() {
        let getOptimizedAuto = function() { 
            return stats.optimizeAuto(blue)
        } // Lazy to avoid it reading only 9999 from the teams

        graphContainerBlue.addGraph(
            "teleopCargoBlue",
            new BarGraph(
                "blueTeleopContainer",
                "Avr. Cycles - Blue",
                {
                    bar: {
                        horizontal: false
                    }
                },
                {
                    formula: {
                    "Cycles": function(team) {return stats.getAvrStat(team, Queries.TELEOP_GRID)}
                    },
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "autoPOTBlue",
            new LineGraph(
                "blueAutoContainer",
                "Auto POT - Blue",
                {},
                {
                    formula: function(team) {return stats.getAvrGridScore(team, Queries.AUTONOMOUS)},
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "autoChargeStationPOTBlue",
            new LineGraph(
                "blueAutoContainer",
                "Auto Charge Station POT - Blue",
                {},
                {
                    formula: function(team) { 
                        return stats.getScoreDataCrit(team, Queries.AUTO_CHARGING_STATE, Queries.AUTO_CHARGE_STATION_CRIT)
                    },
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "autoEngageBlue",
            new StackedBarGraph(
                "blueAutoContainer",
                "Auto Engage Stats - Blue",
                {},
                {
                    formula: function(team) { 
                        let successfulEngages = stats.getScoreDataCrit(team, Queries.AUTO_CHARGING_STATE, Queries.ENGAGE_CRIT)[1].reduce((a, b) => a + b)
                        let successfulDocks = stats.getScoreDataCrit(team, Queries.AUTO_CHARGING_STATE, Queries.DOCKED_CRIT)[1].reduce((a, b) => a + b)
                        let engageMissed = (
                            stats.getScoreDataCrit(team, Queries.AUTO_ATTEMPTED_CHARGING_STATE, Queries.ENGAGE_CRIT)[1].reduce((a, b) => a + b)
                            - successfulEngages
                            - successfulDocks
                        )
                        return [
                            successfulEngages,
                            successfulDocks,
                            engageMissed
                        ]

                    },
                    fields: ["# Of Successful Engages", "# of Docks", "# of Missed Engages"],
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "autoAccuracyBlue",
            new StackedBarGraph(
                "blueAutoContainer",
                "Auto Accuracy - Blue",
                {},
                {
                    formula: function(team) { 
                        let totalAutoCycles = stats.getCumulativeStat(team, Queries.AUTO_GRID)
                        let totalAutoMisses = stats.getCumulativeStat(team, Queries.AUTO_MISSES)
                        return [
                            totalAutoCycles.reduce((a, b) => a + b),
                            totalAutoMisses.reduce((a, b) => a + b)
                        ]
                    },
                    fields: ["Total Auto Cycles", "Total Auto Misses"],
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "teleopPOTBlue",
            new LineGraph(
                "blueTeleopContainer",
                "Teleop POT - Blue",
                {},
                {
                    formula: function(team) {return stats.getAvrGridScore(team, Queries.TELEOP)},
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "breakdown of POINTS ADDED",
            new StackedBarGraph(
                "blueTeleopContainer",
                "Breakdown of Points Added by Team",
                {},
                {
                    formula: function(team) { 
                        let pointsAcrossAuto = stats.getPointsAddedByMatch(team, false, true)
                        let pointsAcrossTeleop = stats.getPointsAddedByMatch(team, false, false, true)
                        let totalPoints =  stats.getPointsAddedByMatch(team, true)

                        let averageAutoPoints = pointsAcrossAuto.reduce((a, b) => a + b) / pointsAcrossAuto.length
                        let averageTeleopPoints = pointsAcrossTeleop.reduce((a, b) => a + b) / pointsAcrossTeleop.length
                        let averageTotalPoints = totalPoints.reduce((a, b) => a + b) / totalPoints.length

                        let breakdownOfPointsAdded = [
                            averageAutoPoints.toFixed(2),
                            averageTeleopPoints.toFixed(2),
                            (averageTotalPoints - (averageAutoPoints + averageTeleopPoints)).toFixed(2)
                        ]

                        return breakdownOfPointsAdded
                    },
                    fields: ["Auto Contribution (pts.)", "Teleop Contribution (pts.)", "Endgame Contribution (pts.)"],
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS,
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "auto CYCLES over time",
            new LineGraph(
                "blueAutoContainer",
                "Auto CYCLES over time - Blue",
                {},
                {
                    formula: function(team) { return stats.getAvrStatOverTime(team, Queries.AUTO_GRID)},
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "teleop CYCLES over time",
            new LineGraph(
                "blueTeleopContainer",
                "Teleop CYCLES over time - Blue",
                {},
                {
                    formula: function(team) { return stats.getAvrStatOverTime(team, Queries.TELEOP_GRID)},
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "teleop CYCLES heatmap",
            new CombinedHeatmap(
                "blueTeleopContainer",
                "Teleop CYCLES Heatmap (Combined) - Blue",
                {},
                {
                    formula: function(team) { return stats.getCycleHeatmapData(team, Queries.TELEOP_GRID)},
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "auto CYCLES heatmap",
            new CombinedHeatmap(
                "blueAutoContainer",
                "Auto CYCLES Heatmap (Combined) - Blue",
                {},
                {
                    formula: function(team) { return stats.getCycleHeatmapData(team, Queries.AUTO_GRID)},
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )
        
        graphContainerBlue.addGraph(
            "score for auto modes OPTIMIZED",
            new BarGraph(
                "blueAutoContainer",
                "Best Possible Autonomous (pts.) - Blue",
                {},
                {
                    formula: {
                        "Left Grid (pts.)": function(team) { 
                            let bestAutoConfig = getOptimizedAuto().filter(value => value[0] == team)[0]
                            return bestAutoConfig[1] == Queries.LEFT ? bestAutoConfig[2] : 0
                        },
                        "Co-Op Grid (pts.)": function(team) { 
                            let bestAutoConfig = getOptimizedAuto().filter(value => value[0] == team)[0]
                            return bestAutoConfig[1] == Queries.COOP ? bestAutoConfig[2] : 0
                        },
                        "Right Grid (pts.)": function(team) { 
                            let bestAutoConfig = getOptimizedAuto().filter(value => value[0] == team)[0]
                            return bestAutoConfig[1] == Queries.RIGHT ? bestAutoConfig[2] : 0
                        }
                    },
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "auto modes OPTIMIZED",
            new CombinedHeatmap(
                "blueAutoContainer",
                "Best Configuration for Autonomous - Blue",
                {},
                {
                    formula: function(team) { 
                        let bestAutoConfig = getOptimizedAuto().filter(value => value[0] == team)[0]
                        return stats.getCycleHeatmapData(team, Queries.AUTO_GRID, stats.data[team][bestAutoConfig[3]][mandatoryMatchData.MATCH_KEY]|| "qm0")
                    },
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )
    }

    // Graphs comparing the Red and Blue alliances here
    function generateComparisonGraphs() {
        let teamsInAlliances = {
            "Blue Alliance": function() { return blue },
            "Red Alliance": function() { return red }
        }
        let oppositeAlliance = {
            "Blue Alliance": function() { return red },
            "Red Alliance": function() { return blue },
        }
        let options = Object.keys(teamsInAlliances)

        // Macro graphs
        graphContainerComparison.addGraph(
            "predicted_scores",
            new AutomatedMacro(
                "macrosContainer", 
                "Predicted Scores", 
                new CompositeStat(
                    [new Factor(function (alliance) { 
                        let compositeStat = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getPointsAddedByMatch(team, true)
                        )
                        return Math.round(compositeStat.reduce((a, b) => a + b) / compositeStat.length)
                    })],
                    100.0,
                ),
                options,
                false
            )
        )

        graphContainerComparison.addGraph(
            "maximum_scores",
            new AutomatedMacro(
                "macrosContainer", 
                "Maximum Scores", 
                new CompositeStat(
                    [new Factor(function (alliance) { 
                        let totalScores = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getPointsAddedByMatch(team, true)
                        )
                        return Math.max(...totalScores)
                    })],
                    100.0,
                ),
                ["Blue Alliance", "Red Alliance"],
                false
            )
        )
        
        graphContainerComparison.addGraph(
            "minimum_scores",
            new AutomatedMacro(
                "macrosContainer", 
                "Minimum Scores", 
                new CompositeStat(
                    [new Factor(function (alliance) { 
                        let totalScores = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getPointsAddedByMatch(team, true)
                        )
                        return Math.min(...totalScores)
                    })],
                    100.0,
                ),
                options,
                false
            )
        )

        graphContainerComparison.addGraph(
            "25p_scores",
            new AutomatedMacro(
                "macrosContainer", 
                "25th Percentile (Bottom 25%) Scores", 
                new CompositeStat(
                    [new Factor(function (alliance) { 
                        let totalScores = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getPointsAddedByMatch(team, true)
                        )
                        return Math.round(
                            stats.quantileSorted(totalScores, 0.25, value => value) 
                        )
                    })],
                    100.0,
                ),
                options,
                false
            )
        )

        graphContainerComparison.addGraph(
            "75p_scores",
            new AutomatedMacro(
                "macrosContainer", 
                "75th Percentile (Top 25%) Scores", 
                new CompositeStat(
                    [new Factor(function (alliance) { 
                        let totalScores = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getPointsAddedByMatch(team, true)
                        )
                        return Math.round(
                            stats.quantileSorted(totalScores, 0.75, value => value) 
                        )
                    })],
                    100.0,
                ),
                options,
                false
            )
        )

        graphContainerComparison.addGraph(
            "total_auto_cycles",
            new AutomatedMacro(
                "macrosContainer", 
                "Average Total Auto Cycles", 
                new CompositeStat(
                    [new Factor(function (alliance) { 
                        let autoCycles = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getCyclesByMatch(team, Queries.AUTO_GRID)
                        )
                        return Math.round(autoCycles.reduce((a, b) => a + b) / autoCycles.length)
                    })],
                    4.0,
                ),
                options,
                false
            )
        )

        graphContainerComparison.addGraph(
            "total_teleop_cycles",
            new AutomatedMacro(
                "macrosContainer", 
                "Average Total Teleop Cycles", 
                new CompositeStat(
                    [new Factor(function (alliance) { 
                        let teleopCycles = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getCyclesByMatch(team, Queries.TELEOP_GRID)
                        )
                        return Math.round(teleopCycles.reduce((a, b) => a + b) / teleopCycles.length)
                    })],
                    9.0,
                ),
                options,
                false
            )
        )
        
        graphContainerComparison.addGraph(
            "chance_of_winning",
            new AutomatedMacro(
                "macrosContainer", 
                "Chance of Winning", 
                new CompositeStat(
                    [new Factor(function (alliance) { 
                        let scoresByTeam = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getPointsAddedByMatch(team, true)
                        )
                        let otherAllianceScores = stats.calculateAllianceCompositeStat(
                            oppositeAlliance[alliance](), 
                            team => stats.getPointsAddedByMatch(team, true)
                        )  
                        var matchesPlayed = 0
                        var matchesWon = 0
                    
                        for (const ownScore of scoresByTeam) {
                            for (const opposingScore of otherAllianceScores) {
                                if (ownScore > opposingScore) {
                                    matchesWon += 1
                                }

                                matchesPlayed += 1
                            }
                        }

                        return matchesWon / matchesPlayed * 100
                    })],
                    50.0,
                ),
                options,
                false,
                true
            )
        )

        // Comparison graphs
        graphContainerComparison.addGraph(
            "auto cycles COMPARED",
            new BoxPlot(
                "alliancesComparedContainer",
                "Total Auto CYCLES over time - Compared",
                {
                    boxPlot: {
                        colors: {
                            upper: '#EFAE04',
                            lower: '#FBC22B'
                        }
                    },
                    bar: {
                        horizontal: true
                    }
                },
                {
                    formula: function(alliance) { 
                        let compositeStat = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getCyclesByMatch(team, Queries.AUTO_GRID)
                        )
                        return [
                            Math.min(...compositeStat),
                            stats.quantileSorted(compositeStat, 0.25, value => value),
                            stats.quantileSorted(compositeStat, 0.5, value => value),
                            stats.quantileSorted(compositeStat, 0.75, value => value),
                            Math.max(...compositeStat)
                        ]
                    },
                    selectedOptions: options,
                    allOptions: options
                },
                modal,
                false
            )
        )

        graphContainerComparison.addGraph(
            "teleop CYCLES COMPARED",
            new BoxPlot(
                "alliancesComparedContainer",
                "Total Teleop CYCLES over time - Compared",
                {
                    boxPlot: {
                        colors: {
                            upper: '#EFAE04',
                            lower: '#FBC22B'
                        }
                    },
                    bar: {
                        horizontal: true
                    }
                },
                {
                    formula: function(alliance) { 
                        let compositeStat = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getCyclesByMatch(team, Queries.TELEOP_GRID)
                        )
                        return [
                            Math.min(...compositeStat),
                            stats.quantileSorted(compositeStat, 0.25, value => value),
                            stats.quantileSorted(compositeStat, 0.5, value => value),
                            stats.quantileSorted(compositeStat, 0.75, value => value),
                            Math.max(...compositeStat)
                        ]
                    },
                    selectedOptions: options,
                    allOptions: options
                },
                modal,
                false
            )
        )

        graphContainerComparison.addGraph(
            "auto POT COMPARED",
            new BoxPlot(
                "alliancesComparedContainer",
                "Total Auto POT - Compared",
                {
                    boxPlot: {
                        colors: {
                            upper: '#EFAE04',
                            lower: '#FBC22B'
                        }
                    },
                    bar: {
                        horizontal: true
                    }
                },
                {
                    formula: function(alliance) { 
                        let compositeStat = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getPointsAddedByMatch(team, false, true)
                        )
                        return [
                            Math.min(...compositeStat),
                            stats.quantileSorted(compositeStat, 0.25, value => value),
                            stats.quantileSorted(compositeStat, 0.5, value => value),
                            stats.quantileSorted(compositeStat, 0.75, value => value),
                            Math.max(...compositeStat)
                        ]
                    },
                    selectedOptions: options,
                    allOptions: options
                },
                modal,
                false
            )
        )

        graphContainerComparison.addGraph(
            "teleop POT COMPARED",
            new BoxPlot(
                "alliancesComparedContainer",
                "Total Teleop POT - Compared",
                {
                    boxPlot: {
                        colors: {
                            upper: '#EFAE04',
                            lower: '#FBC22B'
                        }
                    },
                    bar: {
                        horizontal: true
                    }
                },
                {
                    formula: function(alliance) { 
                        let compositeStat = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getPointsAddedByMatch(team, false, false, true)
                        )
                        return [
                            Math.min(...compositeStat),
                            stats.quantileSorted(compositeStat, 0.25, value => value),
                            stats.quantileSorted(compositeStat, 0.5, value => value),
                            stats.quantileSorted(compositeStat, 0.75, value => value),
                            Math.max(...compositeStat)
                        ]
                    },
                    selectedOptions: options,
                    allOptions: options
                },
                modal,
                false
            )
        )

        graphContainerComparison.addGraph(
            "endgame POT COMPARED",
            new BoxPlot(
                "alliancesComparedContainer",
                "Endgame POT - Compared",
                {
                    boxPlot: {
                        colors: {
                            upper: '#EFAE04',
                            lower: '#FBC22B'
                        }
                    },
                    bar: {
                        horizontal: true
                    }
                },
                {
                    formula: function(alliance) { 
                        let compositeStat = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getScoreDataCrit(team, Queries.TOTAL_ENDGAME, Queries.ENDGAME_CRIT)[1]
                        )
                        return [
                            Math.min(...compositeStat),
                            stats.quantileSorted(compositeStat, 0.25, value => value),
                            stats.quantileSorted(compositeStat, 0.5, value => value),
                            stats.quantileSorted(compositeStat, 0.75, value => value),
                            Math.max(...compositeStat)
                        ]
                    },
                    selectedOptions: options,
                    allOptions: options
                },
                modal,
                false
            )
        )

        graphContainerComparison.addGraph(
            "cumulative POT COMPARED",
            new BoxPlot(
                "alliancesComparedContainer",
                "Cumulative POT - Compared",
                {
                    boxPlot: {
                        colors: {
                            upper: '#EFAE04',
                            lower: '#FBC22B'
                        }
                    },
                    bar: {
                        horizontal: true
                    }
                },
                {
                    formula: function(alliance) { 
                        let compositeStat = stats.calculateAllianceCompositeStat(
                            teamsInAlliances[alliance](), 
                            team => stats.getPointsAddedByMatch(team, true)
                        )
                        return [
                            Math.min(...compositeStat),
                            stats.quantileSorted(compositeStat, 0.25, value => value),
                            stats.quantileSorted(compositeStat, 0.5, value => value),
                            stats.quantileSorted(compositeStat, 0.75, value => value),
                            Math.max(...compositeStat)
                        ]
                    },
                    selectedOptions: options,
                    allOptions: options
                },
                modal,
                false
            )
        )

        graphContainerComparison.addGraph(
            "breakdown of cumulative POT COMPARED",
            new StackedBarGraph(
                "alliancesComparedContainer",
                "Breakdown of Cumulative POT - Compared",
                {},
                {
                    formula: function(alliance) { 
                        var cumulativePOT = []

                        for (const team of teamsInAlliances[alliance]()) {
                            let pointsAcrossMatches = stats.getPointsAddedByMatch(team, true)
                            let averageCumulativePOT = pointsAcrossMatches.reduce((a, b) => a + b) / pointsAcrossMatches.length
                            cumulativePOT.push(averageCumulativePOT.toFixed(2))
                        }

                        return cumulativePOT
                    },
                    fields: ["Robot 1", "Robot 2", "Robot 3"],
                    selectedOptions: options,
                    allOptions: options
                },
                modal,
                false
            )
        )
    }

    document.getElementById("setTeams").addEventListener("click", setTeams)
})()