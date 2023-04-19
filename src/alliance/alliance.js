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
        let avgAutoHighCycles = stats.getAvrTier(team, Queries.HIGH, Queries.AUTO_GRID) * weights["Auto Cycles (High Nodes)"]
        let avgAutoMidCycles = stats.getAvrTier(team, Queries.MID, Queries.AUTO_GRID) * weights["Auto Cycles (Mid Nodes)"]
        let avgAutoHybridCycles = stats.getAvrTier(team, Queries.HYBRID, Queries.AUTO_GRID) * weights["Auto Cycles (Hybrid Nodes)"]
        let avgTeleopHighCycles = stats.getAvrTier(team, Queries.HIGH, Queries.TELEOP_GRID) * weights["Teleop Cycles (High Nodes)"]
        let avgTeleopMidCycles = stats.getAvrTier(team, Queries.MID, Queries.TELEOP_GRID) * weights["Teleop Cycles (Mid Nodes)"]
        let avgTeleopHybridCycles = stats.getAvrTier(team, Queries.HYBRID, Queries.TELEOP_GRID) * weights["Teleop Cycles (Hybrid Nodes)"]
        var cycleData = [avgAutoHighCycles, avgAutoMidCycles, avgAutoHybridCycles, avgTeleopHighCycles, avgTeleopMidCycles, avgTeleopHybridCycles]
        cycleData.push(cycleData.reduce((a, b) => a + b))
        cycleData = cycleData.map(datum => datum.toFixed(1))

        finalCalculations[team] = cycleData
    }

    return finalCalculations
}

(async () => {
    console.log("test")
    var data = await fetch("../lib/chcmp.json").then(res => res.json())
   
    var modal = new Modal("editModal", "fakeToggle", "getEditedData", "editableFormContainer")
    var stats = new CalculatedStats(data)
    
    var factor_matrix = new FactorTable(
        "statsContainer", 
        {
            "Auto Cycles (High Nodes)": [1],
            "Auto Cycles (Mid Nodes)": [1],
            "Auto Cycles (Hybrid Nodes)": [1],
            "Teleop Cycles (High Nodes)": [1],
            "Teleop Cycles (Mid Nodes)": [1],
            "Teleop Cycles (Hybrid Nodes)": [1],
        },
        calculatePicklist,
        modal,
        stats
    )
})()