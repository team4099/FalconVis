import { CalculatedStats } from '../lib/data/CalculatedStats.js';
import { Queries, JSONData, Selections } from '../lib/data/Constants.js'
import { Factor } from '../lib/automated/Factor.js'
import { GraphManager } from '../lib/components/GraphManager.js';
import { AutomatedMacro } from '../lib/components/AutomatedMacro.js';
import { CompositeStat } from '../lib/automated/CompositeStat.js'
import { setTeams, setupTeams, statManager } from './teamParent.js'

(async () => {
    var data = await fetch(JSONData).then(res => res.json())
    var stats = new CalculatedStats(data)
    

    var team = [9999]

    statManager.addGraph(
        "teleop_upper",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. Teleop Upper", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrStat(team,Queries.TELEOP_UPPER_HUB)})],
                2
            ),
            team
        )
    )

    statManager.addGraph(
        "auto_upper",
        new AutomatedMacro(
            "macrosContainer", 
            "Avr. Auto Upper", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrStat(team, Queries.AUTO_UPPER_HUB)})],
                2
            ),
            team
        )
    )

    statManager.addGraph(
        "driver_rating",
        new AutomatedMacro(
            "macrosContainer", 
            "Driver Rating", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrStat(team, Queries.DRIVER_RATING) })],
                2
            ),
            team
        )
    )

    statManager.addGraph(
        "defense_rating",
        new AutomatedMacro(
            "macrosContainer", 
            "Defense Rating", 
            new CompositeStat(
                [new Factor(function (team) { return stats.getAvrStat(team, Queries.DEFENSE_RATING) })],
                2
            ),
            team
        )
    )

    setupTeams(Selections.TEAMS, "teams")
    setTeams(statManager, "teams")
    document.getElementById("teams").addEventListener("change", function () {setTeams(statManager, "teams")})

})()