import { GraphManager } from "../lib/components/GraphManager.js"

var setTeams = function (statManager, id) {
    var team = [document.getElementById(id).value]
    console.log(statManager)
    statManager.pushEditAll(team)
}

var setupTeams = function (teams, id) {
    for (const team of teams){
        document.getElementById(id).innerHTML += `
            <option value=${team}>${team}</option>
        `
    }
}

var statManager = new GraphManager()

export { setTeams, setupTeams, statManager}