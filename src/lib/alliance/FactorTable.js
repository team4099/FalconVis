import { StackedBarGraph } from '../components/StackedBarGraph.js';
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
            this.finalCalculations[team] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }

        // Able to access this reference from elsewhere
        var self = this

        this.statManager = new GraphManager()

        this.statManager.addGraph(
            "picklistGraph",
            new StackedBarGraph(
                "graphContainer",
                "Picklist Rankings (Weighted Cycles)",
                {
                    bar: {
                        horizontal: true,
                        dataLabels: {
                            total: {
                                enabled: true,
                                formatter: label => label.toFixed(1)
                            }
                        }
                    }
                },
                {
                    formula: function (team) { 
                        return self.finalCalculations[team]
                    },
                    fields: ["Auto High", "Auto Mid", "Auto Hybrid", "Teleop High", "Teleop Mid", "Teleop Low"],
                    colors: ["#EFAE09", "#F9D067", "#FBE09C", "#262626", "#6D6D6D", "#ACACAC"],
                    selectedOptions: Object.keys(this.finalCalculations),
                    allOptions: Object.keys(Selections.TEAMS)
                },
                this.modal,
                false,
                true
            )
        )

        document.getElementById(this.parent_id).appendChild(this.companionDiv)

        this.generateTable()

        document.getElementById("tableClick").click()

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
        <div class="flex flex-row gap-2 mt-4">
            <button class="rounded-lg bg-yellow-400 w-28 h-10 text-white text-center pt-1 text-xl font-semibold" id="tableClick">
                Graph
            <button>
            <button class="rounded-lg bg-yellow-400 w-64 h-10 text-white text-center pt-1 text-xl font-semibold" id="usePointage">
                Use Height Pointage
            <button>
        </div>
        `

        var self = this

        document.getElementById("tableClick").addEventListener("click", function () {
            self.pushData()
        })

        document.getElementById("usePointage").addEventListener("click", function () {
            var indexCounter = 0
            let cyclePointages = [6, 4, 3, 5, 3, 2]

            for (const [name, values] of Object.entries(self.factors_pair)) {
                self.factors_pair[name][0] = cyclePointages[indexCounter]
                document.getElementById(values[1]).value = cyclePointages[indexCounter]

                indexCounter += 1
            }
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
            ([,value1],[,value2]) => value2[6] - value1[6]
        ).map(x => x[0])

        this.statManager.pushEditAll(bestTeams)
    }
}