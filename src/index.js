import { BarGraph } from './lib/components/BarGraph.js';
import { LineGraph } from './lib/components/LineGraph.js';
import { ScatterGraph } from './lib/components/ScatterGraph.js';
import { PieGraph } from './lib/components/PieGraph.js';
import { CalculatedStats } from './lib/data/CalculatedStats.js';
import { Selections, Queries, JSONData } from './lib/data/Constants.js';
import { Modal } from './lib/components/Modal.js';

//var data = await fetch('data/iri_data.json').then(response => response.json())

(async () => {
  var data = await fetch(JSONData).then(res => res.json())

  var stats = new CalculatedStats(data)

  var modal = new Modal("editModal", "fakeToggle", "getEditedData", "editableFormContainer")

  var driverRating = new BarGraph(
    "graphContainer",
    "Avg Driver Rating by Team",
    {
      bar: {
        horizontal: false
      }
    },
    {
      formulas: {
        "Auto Upper": function(team) {return stats.getAvgStat(team, Queries.AUTO_UPPER_HUB)},
        "Teleop Upper": function(team) {return stats.getAvgStat(team, Queries.TELEOP_UPPER_HUB)}
      },
      selectedOptions: [4099, 118, 180],
      allOptions: Selections.TEAMS
    },
    modal
  )

  var shooterOverTime = new LineGraph(
    "graphContainer",
    "Shooter over matches",
    {},
    {
      formula: function(team) {return stats.getScoreData(team, Queries.TELEOP_UPPER_HUB)},
      selectedOptions: [2056],
      allOptions: Selections.TEAMS
    },
    modal
  )

  var goodShooters = new ScatterGraph(
    "graphContainer",
    "Shooting by match by team",
    {},
    {
      formulaX: function(team) {return stats.getScoreData(team, Queries.TELEOP_UPPER_HUB)},
      formulaY: function(team) {return stats.getScoreData(team, Queries.AUTO_UPPER_HUB)},
      selectedOptions: [4099, 2056],
      allOptions: Selections.TEAMS
    },
    modal
  )

  var gameContribution = new PieGraph(
    "graphContainer",
    "shooting contrib by match",
    {},
    {
      formula: function(match) {return stats.getMatchAllianceData(match, Queries.TELEOP_UPPER_HUB, Selections.RED)},
      selectedOption: "qm1",
      allOptions: Selections.MATCHES
    },
    modal
  )
})();