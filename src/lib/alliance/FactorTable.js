import { BarGraph } from '../components/BarGraph.js';
import { Selections } from '../data/Constants.js';
import { GraphManager } from '../components/GraphManager.js';
import { Graph } from '../components/Graph.js';

export class FactorTable {
    constructor(parent_id, factors_pair, callback, modal, stats){
        this.uuid = Math.random().toString(36).substr(2, 9)

        this.parent_id = parent_id
        this.factors_pair = factors_pair
        this.onclick = callback
        this.modal = modal
        this.stats = stats

        for (const key of Object.keys(this.factors_pair)){
            this.factors_pair[key].push(0)
        }

        this.companionDiv = document.createElement("table")
        this.companionDiv.classList.add("border-collapse","table-auto","w-full","text-sm")
        this.companionDiv.id = this.uuid
        
        // Bar graph portion of picklist generation
        this.finalCalculations = {}

        for (const team of Selections.TEAMS) {
            this.finalCalculations[team] = 0.0
        }

        // Able to access this reference from elsewhere
        var self = this

        this.statManager = new GraphManager()

        this.statManager.addGraph(
            "picklistGraph",
            new BarGraph(
                "graphContainer",
                "Picklist Rankings (Measure of Their Capability versus their Maximum Potential)",
                {
                    bar: {
                        horizontal: true
                    }
                },
                {
                    formula: {
                        "Offensive Potential": function (team) { 
                            return self.finalCalculations[team].toFixed(1) 
                        }
                    },
                    selectedOptions: Object.keys(this.finalCalculations),
                    allOptions: Object.keys(Selections.TEAMS)
                },
                this.modal,
                true,
                true,
                8
            )
        )

        document.getElementById(this.parent_id).appendChild(this.companionDiv)

        this.generateTable()

    }

    generateTable(){
        this.companionDiv.innerHTML = `
        <thead>
            <tr>
                <th class="border-b font-medium p-4 pt-0 pb-3 text-left">Factor</th>
                <th class="border-b font-medium p-4 pt-0 pb-3 text-left">Rating</th>
            </tr>
        </thead>
        `

        for (const factor of Object.keys(this.factors_pair)){
            this.factors_pair[factor][1] = Math.random().toString(36).substr(2, 9)
            this.companionDiv.innerHTML += `
            <tr>
                <td class="border-b border-slate-100 p-4 text-black">${factor}</td>
                <td class="border-b border-slate-100 p-4 text-black"><input class="border border-2 border-black h-8 pl-2 rounded-md" value=${this.factors_pair[factor][0]} id=${this.factors_pair[factor][1]}></input></td>
            </tr>
            `
        }

        this.companionDiv.innerHTML += `
        <div class="mt-4">
            <div class="rounded-lg w-28 h-10 bg-yellow-400 text-white text-center pt-1 text-xl font-semibold" id="tableClick">
                Graph
            <div>
        </div>
        `

        var self = this

        document.getElementById("tableClick").addEventListener("click", function () {
            self.pushData()
        })
    }

    pushData(){
        var data = {}

        for (const factor of Object.keys(this.factors_pair)){
            data[factor] = parseFloat(document.getElementById(this.factors_pair[factor][1]).value)
        }

        let finalCalculations = this.onclick(data, this.stats)
        this.finalCalculations = finalCalculations
        
        // Sort picklist rankings
        let bestTeams = Object.entries(finalCalculations).sort(
            ([,value1],[,value2]) => value2 - value1
        ).map(x => x[0])

        this.statManager.pushEditAll(bestTeams)
    }
}