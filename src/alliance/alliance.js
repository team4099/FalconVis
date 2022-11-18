import { CalculatedStats } from '../lib/data/CalculatedStats.js';
import { PickTable } from '../lib/components/PickTable.js';
import { Queries, JSONData } from '../lib/data/Constants.js'
import { WeightedStat } from '../lib/automated/WeightedStat.js'
import { Factor } from '../lib/automated/Factor.js'

(async () => {
    var data = await fetch(JSONData).then(res => res.json())

    var stats = new CalculatedStats(data)

    var pickOrderTable = new PickTable("pickTable", data);
    
    var pickOrderSort = function(){
        pickOrderTable.sortByFalconRank()
    }
    var metricSort = function(){
        pickOrderTable.sortByMetric(Queries.TELEOP_UPPER_HUB)
    }
    
    var updateRanking = function () {
       // document.getElementById("pickTable").innerHTML = ''
        var mode = document.getElementById("allianceMode").value
        if (mode == "pickOrder"){
            pickOrderSort();
        }else{
            metricSort();
        }
    }
    
    
    updateRanking()

    document.getElementById("allianceMode").addEventListener("change", updateRanking)

})()