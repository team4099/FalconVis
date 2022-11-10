import { CalculatedStats } from '../lib/data/CalculatedStats.js';
import { Queries, Selections, JSONData } from '../lib/data/Constants.js'
import { BarGraph } from '../lib/components/BarGraph.js';
import { LineGraph } from '../lib/components/LineGraph.js';
import { Modal } from '../lib/components/Modal.js';


(async () => {
    var data = await fetch(JSONData).then(res => res.json())
    var stats = new CalculatedStats(data)
    var modal = new Modal("editModal", "fakeToggle", "getEditedData", "editableFormContainer")

    var red = [9999, 9999, 9999]
    var blue = [9999, 9999, 9999]

    var teleopCargoBlue = new BarGraph(
        "blueAllianceContainer",
        "Avr. Teleop Cargo - Blue",
        {
            bar: {
                horizontal: false
            }
        },
        {
            formulas: {
              "Teleop Lower": function(team) {return stats.getAvgStat(team, Queries.TELEOP_LOWER_HUB)},
              "Teleop Upper": function(team) {return stats.getAvgStat(team, Queries.TELEOP_UPPER_HUB)}
            },
            selectedOptions: blue,
            allOptions: Selections.TEAMS
        },
        modal,
        false
    )

    var teleopPOTBlue = new LineGraph(
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

    var defenseBlue = new BarGraph(
        "blueAllianceContainer",
        "Defense - Blue",
        {
            bar: {
                horizontal: false
            }
        },
        {
            formulas: {
              "Defense Rating": function(team) {return stats.getAvgStat(team, Queries.DEFENSE_RATING)},
              "Counter Def Rating": function(team) {return stats.getAvgStat(team, Queries.COUNTER_DEFENSE_RATING)},
              "Driver Rating": function(team) {return stats.getAvgStat(team, Queries.DRIVER_RATING)}
            },
            selectedOptions: blue,
            allOptions: Selections.TEAMS
        },
        modal,
        false
    )

    var teleopCargoRed = new BarGraph(
        "redAllianceContainer",
        "Avr. Teleop Cargo - Red",
        {
            bar: {
                horizontal: false
            }
        },
        {
            formulas: {
              "Teleop Lower": function(team) {return stats.getAvgStat(team, Queries.TELEOP_LOWER_HUB)},
              "Teleop Upper": function(team) {return stats.getAvgStat(team, Queries.TELEOP_UPPER_HUB)}
            },
            selectedOptions: red,
            allOptions: Selections.TEAMS
        },
        modal,
        false
    )

    var teleopPOTRed = new LineGraph(
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

    var defenseRed = new BarGraph(
        "redAllianceContainer",
        "Defense - Red",
        {
            bar: {
                horizontal: false
            }
        },
        {
            formulas: {
              "Defense Rating": function(team) {return stats.getAvgStat(team, Queries.DEFENSE_RATING)},
              "Counter Def Rating": function(team) {return stats.getAvgStat(team, Queries.COUNTER_DEFENSE_RATING)},
              "Driver Rating": function(team) {return stats.getAvgStat(team, Queries.DRIVER_RATING)}
            },
            selectedOptions: red,
            allOptions: Selections.TEAMS
        },
        modal,
        false
    )

    var setTeams = () => {
        blue = [
            parseInt(document.getElementById("blue1").value),
            parseInt(document.getElementById("blue2").value),
            parseInt(document.getElementById("blue3").value),
        ]

        red = [
            parseInt(document.getElementById("red1").value),
            parseInt(document.getElementById("red2").value),
            parseInt(document.getElementById("red3").value),
        ]

        teleopCargoBlue.pushEdit(false, blue)
        teleopPOTBlue.pushEdit(false, blue)
        defenseBlue.pushEdit(false, blue)

        teleopCargoRed.pushEdit(false, red)
        teleopPOTRed.pushEdit(false, red)
        defenseRed.pushEdit(false, red)
    }

    document.getElementById("setTeams").addEventListener("click", setTeams)

})()