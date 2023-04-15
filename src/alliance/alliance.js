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
        let pointsAddedByMatch = stats.getPointsAddedByMatch(team)
        finalCalculations[team] = pointsAddedByMatch.reduce((a, b) => a + b) / pointsAddedByMatch.length
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