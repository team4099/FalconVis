import { Queries, Selections, JSONData } from '../lib/data/Constants.js'
import { BarGraph } from '../lib/components/BarGraph.js';
import { LineGraph } from '../lib/components/LineGraph.js';
import { AutomatedMacro } from '../lib/components/AutomatedMacro.js';
import { WeightedStat } from '../lib/automated/WeightedStat.js'
import { Factor } from '../lib/automated/Factor.js'
import { CalculatedStats } from '../lib/data/CalculatedStats.js';
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

    generateBlueGraphs(stats)
    generateRedGraphs(stats)

    // Red Graphs Generated Here
    function generateRedGraphs(stats){
        graphContainerRed.addGraph(
            "teleopCargoRed",
            new BarGraph(
                "redAllianceContainer",
                "Avr. Teleop Cargo - Red",
                {
                    bar: {
                        horizontal: false
                    }
                },
                {
                    formulas: {
                    "Teleop Lower": function(team) {return stats.getAvrStat(team, Queries.TELEOP_LOWER_HUB)},
                    "Teleop Upper": function(team) {return stats.getAvrStat(team, Queries.TELEOP_UPPER_HUB)}
                    },
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
                formula: function(team) {return stats.getTotalPoints(team, Queries.TELEOP_TOTAL)},
                selectedOptions: red,
                allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "defenseRed",
            new BarGraph(
                "redAllianceContainer",
                "Defense - Red",
                {
                    bar: {
                        horizontal: false
                    }
                },
                {
                    formulas: {
                    "Defense Rating": function(team) {return stats.getAvrStat(team, Queries.DEFENSE_RATING)},
                    "Counter Def Rating": function(team) {return stats.getAvrStat(team, Queries.COUNTER_DEFENSE_RATING)},
                    "Driver Rating": function(team) {return stats.getAvrStat(team, Queries.DRIVER_RATING)}
                    },
                    selectedOptions: red,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerRed.addGraph(
            "defenseAutomatedRed",
            new AutomatedMacro(
                "redAllianceContainer",
                "Defense Options Auto",
                defenseStat,
                red
            )
        )
    }

    // Blue Graphs Generated Here
    function generateBlueGraphs(stats){
        graphContainerBlue.addGraph(
            "teleopCargoBlue", 
            new BarGraph(
                "blueAllianceContainer",
                "Avr. Teleop Cargo - Blue",
                {
                    bar: {
                        horizontal: false
                    }
                },
                {
                    formulas: {
                    "Teleop Lower": function(team) {return stats.getAvrStat(team, Queries.TELEOP_LOWER_HUB)},
                    "Teleop Upper": function(team) {return stats.getAvrStat(team, Queries.TELEOP_UPPER_HUB)}
                    },
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
                "blueAllianceContainer",
                "Teleop POT - Blue",
                {},
                {
                formula: function(team) {return stats.getTotalPoints(team, Queries.TELEOP_TOTAL)},
                selectedOptions: blue,
                allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "defenseBlue",
            new BarGraph(
                "blueAllianceContainer",
                "Defense - Blue",
                {
                    bar: {
                        horizontal: false
                    }
                },
                {
                    formulas: {
                    "Defense Rating": function(team) {return stats.getAvrStat(team, Queries.DEFENSE_RATING)},
                    "Counter Def Rating": function(team) {return stats.getAvrStat(team, Queries.COUNTER_DEFENSE_RATING)},
                    "Driver Rating": function(team) {return stats.getAvrStat(team, Queries.DRIVER_RATING)}
                    },
                    selectedOptions: blue,
                    allOptions: Selections.TEAMS
                },
                modal,
                false
            )
        )

        graphContainerBlue.addGraph(
            "defenseAutomatedBlue",
            new AutomatedMacro(
                "blueAllianceContainer",
                "Defense Options Auto",
                defenseStat,
                blue
            )
        )
    }

    document.getElementById("setTeams").addEventListener("click", setTeams)
})()