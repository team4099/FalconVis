import { Queries, Selections, JSONData } from '../lib/data/Constants.js'
import { BarGraph } from '../lib/components/BarGraph.js';
import { LineGraph } from '../lib/components/LineGraph.js';
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
    graphContainerRed, red, blue 
} from './matchParent.js'


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
    
    // Red Graphs Generated Here
    function generateRedGraphs(){
        graphContainerRed.addGraph(
            "teleopCargoRed",
            new BarGraph(
                "redAllianceContainer",
                "Avr. Cycles Cargo - Red",
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
                "redAllianceContainer",
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
            "teleopPOTRed",
            new LineGraph(
                "redAllianceContainer",
                "Teleop POT - Red",
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

        graphContainerRed.addGraph(
            "auto CYCLES over time",
            new LineGraph(
                "redAllianceContainer",
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
                "redAllianceContainer",
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
                "redAllianceContainer",
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
                "redAllianceContainer",
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
    }

// Blue Graphs Generated Here
    function generateBlueGraphs(){
        graphContainerBlue.addGraph(
            "teleopCargoBlue",
            new BarGraph(
                "blueAllianceContainer",
                "Avr. Cycles Cargo - Blue",
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
                "blueAllianceContainer",
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
            "teleopPOTRed",
            new LineGraph(
                "blueAllianceContainer",
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
            "auto CYCLES over time",
            new LineGraph(
                "blueAllianceContainer",
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
                "blueAllianceContainer",
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
                "blueAllianceContainer",
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
                "blueAllianceContainer",
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
    }

    document.getElementById("setTeams").addEventListener("click", setTeams)
})()