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

(async () => {
    console.log("test")
    var data = await fetch(JSONData).then(res => res.json())
    var stats = new CalculatedStats(data)
    var modal = new Modal("editModal", "fakeToggle", "getEditedData", "editableFormContainer")

    var team = [Selections.TEAMS[0]]

    
    statManager.addGraph(
        "avr_cycles",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. Cycles Count", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrStat(team,mandatoryMatchData.AUTO_GRID)})],
                5
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
                [new Factor(function (team) { return stats.getScoreDataCritSingle(team,Queries.MOBILITY, Queries.MOBILITY_CRIT)})],
                50.00
            ),
            team
        )
    )

    statManager.addGraph(
        "avr_cycles",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. Auto Accuracy (Pcnt)", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrGridMissed(team,Queries.AUTONOMOUS)})],
                80
            ),
            team
        )
    )

    statManager.addGraph(
        "avr_cycles",
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
        "avr_cycles",
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
                    "High Avr": function(team) { return stats.getAvrTier(team, Queries.HIGH)},
                    "Mid Avr": function(team) { return stats.getAvrTier(team, Queries.MID)},
                    "Hybrid Avr": function(team) { return stats.getAvrTier(team, Queries.HYBRID)}
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
        "auto grid score over time",
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
                    "Left grid": function(team) { return stats.getAvrGrid(team, Queries.LEFT)},
                    "Coop grid": function(team) { return stats.getAvrGrid(team, Queries.COOP)},
                    "Right grid": function(team) { return stats.getAvrGrid(team, Queries.RIGHT)}
                },
                selectedOptions: team,
                allOptions: Selections.TEAMS
            },
            modal,
            false
        )
    )

    setupTeams(Selections.TEAMS, "teams")
    setTeams(statManager, "teams")
    document.getElementById("teams").addEventListener("change", function () {setTeams(statManager, "teams")})

})()