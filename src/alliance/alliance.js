import { CalculatedStats } from '../lib/data/CalculatedStats.js';
import { Queries, JSONData, Selections } from '../lib/data/Constants.js'
import { Modal } from '../lib/components/Modal.js';
import { FactorTable } from '../lib/alliance/FactorTable.js';

(async () => {
    console.log("test")
    //var data = await fetch(JSONData).then(res => res.json())
    //var stats = new CalculatedStats(data)
    var modal = new Modal("editModal", "fakeToggle", "getEditedData", "editableFormContainer")
    //console.log(stats.data)
    
    var factor_matrix = new FactorTable("statsContainer", {"test": [1.0], "tester": [2.0]}, function () {})
})()