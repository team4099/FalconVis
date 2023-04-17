import { CalculatedStats } from '../lib/data/CalculatedStats.js';
import { Queries, JSONData, Selections, mandatoryMatchData } from '../lib/data/Constants.js'
import { Modal } from '../lib/components/Modal.js';
import { statManager } from './eventParent.js'
import { BoxPlot } from '../lib/components/BoxPlot.js';

(async () => {
    console.log("test")
    var data = await fetch(JSONData).then(res => res.json())
    var stats = new CalculatedStats(data)
    var modal = new Modal("editModal", "fakeToggle", "getEditedData", "editableFormContainer")
    console.log(stats.data)

    statManager.addGraph(
        "Point Contributions DISTRIBUTIONS by TEAM",
        new BoxPlot(
            "graphContainer",
            "Point Contribution (without Endgame) Distributions By Team",
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
                formula: function(team) {
                    let pointsContributed = stats.getPointsAddedByMatch(team)
                    return [
                        Math.min(...pointsContributed), 
                        stats.quantileSorted(pointsContributed, 0.25, value => value),
                        stats.quantileSorted(pointsContributed, 0.5, value => value),
                        stats.quantileSorted(pointsContributed, 0.75, value => value),
                        Math.max(...pointsContributed)
                    ]
                },
                selectedOptions: Selections.TEAMS,
                allOptions: Selections.TEAMS
            },
            modal,
            true,
            true
        )
    )

    statManager.addGraph(
        "Cycle DISTRIBUTIONS by TEAM",
        new BoxPlot(
            "graphContainer",
            "Cycle Distributions By Team",
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
                formula: function(team) {
                    let totalCycles = stats.getCyclesByMatch(team, Queries.TELEOP_GRID)
                    return [
                        Math.min(...totalCycles), 
                        stats.quantileSorted(totalCycles, 0.25, value => value),
                        stats.quantileSorted(totalCycles, 0.5, value => value),
                        stats.quantileSorted(totalCycles, 0.75, value => value),
                        Math.max(...totalCycles)
                    ]
                },
                selectedOptions: Selections.TEAMS,
                allOptions: Selections.TEAMS
            },
            modal,
            true,
            true
        )
    )

})()