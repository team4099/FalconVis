import { CalculatedStats } from '../lib/data/CalculatedStats.js';
import { Queries, JSONData, Selections } from '../lib/data/Constants.js'
import { Modal } from '../lib/components/Modal.js';
import { BarGraph } from '../lib/components/BarGraph.js';
import { FactorTable } from '../lib/alliance/FactorTable.js';

// Calculates the picklist based off weights passed in
function returnRankings() {
    return [
        ['Aanshi Patel', 0], 
        ['Shashwat  Dixit', 0], 
        ['Saragha Surendra', 2], 
        ['Ryan Lo', 4], 
        ['Neel Bhattacharyya', 6], 
        ['Hannah Chen', 8], 
        ['Sanjay Tamil', 8], 
        ['rachel zhang', 8], 
        ['Joshua Tang', 8], 
        ['Wack Zac', 8], 
        ['Srinidhi Guruvayurappan', 10], 
        ['Agneya Tharun', 12], 
        ['Sydney Saeed', 14], 
        ['Brandon Kim', 14], 
        ['Rithvik Kondragunta', 14], 
        ['Sayan Chandaroy', 16], 
        ['Aran Jaiman', 16], 
        ['Matthew Choulas', 18], 
        ['Sarah Yu', 18], 
        ['Ryan Zhao', 22], 
        ['Shayaan Wadkar', 22], 
        ['Eckart  Schneider', 24]
    ].reverse()
}

(async () => {
    console.log("test")
    var data = await fetch("https://raw.githubusercontent.com/team4099/ScoutingAppData/main/chcmp_rankings.json").then(res => res.json())
   
    var modal = new Modal("editModal", "fakeToggle", "getEditedData", "editableFormContainer")
    
    var teamRankings = returnRankings()

    var companionDiv = document.getElementById("rankcon")
    companionDiv.classList.add("border-collapse","table-auto","w-full","text-sm")

    companionDiv.innerHTML = `
        <thead>
            <tr>
                <th class="border-b font-medium p-4 pt-0 pb-3 text-left">Name</th>
                <th class="border-b font-medium p-4 pt-0 pb-3 text-left">Score</th>
            </tr>
        </thead>
        `

    var count = 1
    for (const factor of teamRankings){
        companionDiv.innerHTML += `
        <tr>
            <td class="border-b border-slate-100 p-4 text-black">${count}. ${factor[0]}</td>
            <td class="border-b border-slate-100 p-4 text-black">${factor[1]}</td>
        </tr>
        `
        count += 1
    }
    
})()