import { CalculatedStats } from '../lib/data/CalculatedStats.js';
import { Queries, JSONData, Selections } from '../lib/data/Constants.js'
import { Modal } from '../lib/components/Modal.js';
import { BarGraph } from '../lib/components/BarGraph.js';
import { FactorTable } from '../lib/alliance/FactorTable.js';
import { statManager } from './allianceParent.js';

// Calculates the picklist based off weights passed in
function calculatePicklist(weights, stats) {
    let teams = Object.keys(stats.data)
    var finalCalculations = {}

    for (const team of teams) {
        let weightsToMaximum = {
            "Auto Cycles": 5,
            "Teleop Cycles (High Nodes)": 9,
            "Teleop Cycles (Mid Nodes)": 9,
            "Teleop Cycles (Hybrid Nodes)": 9,
            "Total Endgame Engages": stats.data[team].length,
            "Interquartile Range (# of Teleop Cycles)": 0,
            "Disables": 0
        }
        
        let averageAutoCycles = stats.getAvrGrid(team, null, Queries.AUTO_GRID)
        let averageHighCycles = stats.getAvrTier(team, Queries.HIGH, Queries.TELEOP_GRID)
        let averageMidCycles = stats.getAvrTier(team, Queries.MID, Queries.TELEOP_GRID)
        let averageHybridCycles = stats.getAvrTier(team, Queries.HYBRID, Queries.TELEOP_GRID)
        let totalEngages = stats
            .getScoreDataCrit(team, Queries.TOTAL_ENDGAME, Queries.ENGAGE_CRIT)[1]
            .filter( Number )
            .reduce((a, b) => a + b, 0)
        let totalDisables = stats
            .getScoreDataCrit(team, Queries.DISABLED, Queries.DISABLED_CRIT)[1]
            .reduce((a, b) => a + b, 0)

        let totalCycles = stats.getCyclesByMatch(team, Queries.TELEOP_GRID)
        let interQuartileRange = stats.quantileSorted(totalCycles, 0.75, value => value) - stats.quantileSorted(totalCycles, 0.25, value => value)
        let allWeights = [averageAutoCycles, averageHighCycles, averageMidCycles, averageHybridCycles, totalEngages, interQuartileRange, totalDisables]
        
        // Calculate weights
        var counter = 0
        var totalCalculations = 0
        var possibleMaximum = 0
        
        for (const [weightName, maximum] of Object.entries(weightsToMaximum)) {
            totalCalculations += allWeights[counter] * weights[weightName]
            possibleMaximum += maximum * weights[weightName]
            counter += 1
        }

        finalCalculations[team] = (totalCalculations / possibleMaximum) * 100
    }

    return finalCalculations
}

(async () => {
    var data = await fetch(JSONData).then(res => res.json())
    var modal = new Modal("editModal", "fakeToggle", "getEditedData", "editableFormContainer")
    var stats = new CalculatedStats(data)
    
    var factor_matrix = new FactorTable(
        "statsContainer", 
        {
            "Auto Cycles": [0.5],
            "Teleop Cycles (High Nodes)": [1],
            "Teleop Cycles (Mid Nodes)": [0.75],
            "Teleop Cycles (Hybrid Nodes)": [0.5],
            "Total Endgame Engages": [0.5],
            "Interquartile Range (# of Teleop Cycles)": [-1],
            "Disables": [-1]
        },
        calculatePicklist,
        modal,
        stats
    )
})()