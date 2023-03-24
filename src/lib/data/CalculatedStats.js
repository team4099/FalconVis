import { mandatoryMatchData, Queries } from "../data/Constants.js"

class CalculatedStats {
    constructor(data){
        this.old_data = data
        this.data = {}

        for (const entry of this.old_data){
            entry[mandatoryMatchData.AUTO_GRID] = entry[mandatoryMatchData.AUTO_GRID].split("|")
            entry[mandatoryMatchData.TELEOP_GRID] = entry[mandatoryMatchData.TELEOP_GRID].split("|")

            if (Object.keys(this.data).includes(entry[mandatoryMatchData.TEAM_NUMBER].toString())){
                this.data[entry[mandatoryMatchData.TEAM_NUMBER]].push(entry)
            }
            else {
                this.data[entry[mandatoryMatchData.TEAM_NUMBER]] = [entry]
            }
        }

        for (const team of Object.keys(this.data)){
            this.data[team].sort(function(a,b){
                return parseInt(a[mandatoryMatchData.MATCH_KEY].slice(2)) -
                parseInt(b[mandatoryMatchData.MATCH_KEY].slice(2))
            });
        }

        console.log(this.data)
    }

    getAvrGridScore(team, section){
        try {
            console.log("getAvrGridScore")
            var match = []
            var scored = []

            if (section == Queries.AUTONOMOUS){
                var type = Queries.AUTO_GRID
                var grid_crit = Queries.AUTO_GRID_SCORE
            }
            else {
                var type = Queries.TELEOP_GRID
                var grid_crit = Queries.TELEOP_GRID_SCORE
            }
            
            var count = 0
            for (const x of this.data[team]) { 
                match.push(count)
                count += 1
                var totalSum = 0
                for (const score of x[type]){
                    totalSum += grid_crit[score[1]]
                }
                if (Number.isNaN(totalSum)){
                    scored.push(0)
                }
                else {
                    scored.push(totalSum)
                }
                console.log(scored)
            }
            console.log(scored)
            return [match, scored]
        }
        catch (e) {
            console.log(e, this.data[team])
            return [[0], [0]]
        }
    }

    getAvrGridMissed(team, section){
        try {
            var values = 0
            var count = 0
        
            for (const x of this.data[team]) { 
                if (section == Queries.AUTONOMOUS){
                    values += (x[Queries.AUTO_GRID].length / (x[Queries.AUTO_GRID].length +x[Queries.AUTO_MISSES] + 1))*100
                    count += 1
                }
                else {
                    values += (x[Queries.TELEOP_GRID].length / (x[Queries.TELEOP_GRID].length +x[Queries.TELEOP_MISSES]))*100
                    count += 1
                }
                
            }

            console.log(values, count)

            return (values/count).toFixed(2)
        }
        catch (e) {
            return 0
        }
    }

    getAvrStatOverTime(team, stat){
        try {
            var match = []
            var scored = []
        
            var count = 0
            for (const x of this.data[team]) { 
                if (typeof(x[stat]) == "object"){
                    match.push(count)
                    scored.push(x[stat].length)
                }
                else {
                    match.push(count)
                    scored.push(0)
                }
                count += 1
            }

            return [match, scored]
        }
        catch (e) {
            return [[0], [0]]
        }
    }

    getAvrStat(team, stat){
        try {
            var values = 0
            var count = 0
        
            for (const x of this.data[team]) { 
                if (typeof(x[stat]) == "object"){
                    values += x[stat].length
                }
                else {
                    values += x[stat]
                }
                count += 1
            }

            return (values/count).toFixed(2)
        }
        catch (e) {
            return 0
        }
    }

    getTotalPoints(team, stat){
        try {
            var match = []
            var scored = []
            var temp = 0
        
            for (const x of this.data[team]) { 
                temp = 0
                for (const component of Object.keys(stat)){
                    temp += x[component]*stat[component]
                }
                match.push(x[mandatoryMatchData.MATCH_KEY])
                scored.push(temp)
            }
    
            return [match, scored]
        }
        catch (e) {
            return [[0], [0]]
        }
    }

    getAvrGrid(team, stat){
        try {
            var count = 0
            for (const x of this.data[team]) { 
                for (const score of x[mandatoryMatchData.AUTO_GRID]){
                    if (stat == Queries.LEFT){
                        if (["1", "2", "3"].includes(score[0])){
                            count += 1
                        }
                        
                    }
                    if (stat == Queries.COOP){
                        if (["4", "5", "6"].includes(score[0])){
                            count += 1
                        }
                    }
                    if (stat == Queries.RIGHT){
                        if (["7", "8", "9"].includes(score[0])){
                            count += 1
                        }
                    }
                }    
            }

            return count
        }
        catch (e) {
            return 0
        }
    }

    getAvrTier(team, stat){
        try {
            var count = 0
            for (const x of this.data[team]) { 
                for (const score of x[mandatoryMatchData.AUTO_GRID]){
                    if (stat == Queries.HIGH && score[1] == "H"){
                        count += 1
                        
                    }
                    if (stat == Queries.MID && score[1] == "M"){
                        count += 1
                        
                    }
                    if (stat == Queries.HYBRID && score[1] == "L"){
                        count += 1
                    }
                }    
            }
            return (count).toFixed(2)
        }
        catch (e) {
            console.log(e, team)
            return 0
        }
    }

    getScoreDataCrit(team, stat_comp, stat_crit){
        try {
            var match = []
            var scored = []
        
            for (const x of this.data[team]) { 
                match.push(x[mandatoryMatchData.MATCH_KEY])
                scored.push(stat_crit[x[stat_comp]])
            }
    
            return [match, scored]
        }
        catch (e) {
            return [[0], [0]]
        }
    }

    getScoreDataCritSingle(team, stat_comp, stat_crit){
        try {
            var match = []
            var scored = 0
        
            for (const x of this.data[team]) { 
                match.push(x[mandatoryMatchData.MATCH_KEY])
                scored += stat_crit[x[stat_comp]]
            }
    
            return scored / match.length
        }
        catch (e) {
            return 0
        }
    }

    getMatchAllianceData(match, stat, alliance){
        try {
            var teams = []
            var scored = []
        
            for (const x of Object.values(this.data)) {
                for (const l of x){
                    if (l[mandatoryMatchData.MATCH_KEY] == match && l[mandatoryMatchData.ALLIANCE] == alliance){
                        teams.push(l[mandatoryMatchData.TEAM_NUMBER].toString())
                        scored.push(l[stat])
                        break
                    }
                }
            }
    
            return [teams, scored]
        }
        catch (e) {
            console.log(e)
            return [[0], [0]]
        }
    }

    getCycleHeatmapData(team, heatmapGrid) {
        var positionsToIndices = {
            "H": 0,
            "M": 1,
            "L": 2
        }
        var indicesToNames = ["High", "Mid", "Bottom"]
        var indicesToLocations = ["Cone1", "Cube2", "Cone3", "Cone4", "Cube5", "Cone6", "Cone7", "Cube8", "Cone9"]

        var cycleHeatmap = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        var heatmapFormatted = []

        try {
            for (const matchData of this.data[team]) {
                if (matchData[heatmapGrid][0] != "") {
                    for (const gamePiece of matchData[heatmapGrid]) {
                        let gamePieceX = parseInt(gamePiece[0]) - 1
                        let gamePieceY = gamePiece[1]

                        if (matchData["Alliance"] == "red") {
                            gamePieceX = 9 - gamePieceX - 1
                        }

                        cycleHeatmap[positionsToIndices[gamePieceY]][gamePieceX] += 1
                    }
                }
            }
            
            for (const row of cycleHeatmap) {
                var currentIndex = cycleHeatmap.indexOf(row)
                var rowData = []

                for (let counter = 0; counter < indicesToLocations.length; counter++) {
                    rowData.push({
                        "x": indicesToLocations[counter],
                        "y": row[counter]
                    })
                }

                heatmapFormatted.push(
                    {
                        "name": indicesToNames[currentIndex],
                        "data": rowData
                    }
                )
            }
        }
        catch (e) {
            console.log(e)

            return [
                {
                    "name": "High",
                    "data": [
                        {
                            "x": "Cone1",
                            "y": 0
                        },
                        {
                            "x": "Cube2",
                            "y": 0
                        },
                        {
                            "x": "Cone3",
                            "y": 0
                        },
                        {
                            "x": "Cone4",
                            "y": 0
                        },
                        {
                            "x": "Cube5",
                            "y": 0
                        },
                        {
                            "x": "Cone6",
                            "y": 0
                        },
                        {
                            "x": "Cone7",
                            "y": 0
                        },
                        {
                            "x": "Cube8",
                            "y": 0
                        },
                        {
                            "x": "Cone9",
                            "y": 0
                        }
                    ]
                },
                {
                    "name": "Mid",
                    "data": [
                        {
                            "x": "Cone1",
                            "y": 0
                        },
                        {
                            "x": "Cube2",
                            "y": 0
                        },
                        {
                            "x": "Cone3",
                            "y": 0
                        },
                        {
                            "x": "Cone4",
                            "y": 0
                        },
                        {
                            "x": "Cube5",
                            "y": 0
                        },
                        {
                            "x": "Cone6",
                            "y": 0
                        },
                        {
                            "x": "Cone7",
                            "y": 0
                        },
                        {
                            "x": "Cube8",
                            "y": 0
                        },
                        {
                            "x": "Cone9",
                            "y": 0
                        }
                    ]
                },
                {
                    "name": "Bottom",
                    "data": [
                        {
                            "x": "Cone1",
                            "y": 0
                        },
                        {
                            "x": "Cube2",
                            "y": 0
                        },
                        {
                            "x": "Cone3",
                            "y": 0
                        },
                        {
                            "x": "Cone4",
                            "y": 0
                        },
                        {
                            "x": "Cube5",
                            "y": 0
                        },
                        {
                            "x": "Cone6",
                            "y": 0
                        },
                        {
                            "x": "Cone7",
                            "y": 0
                        },
                        {
                            "x": "Cube8",
                            "y": 0
                        },
                        {
                            "x": "Cone9",
                            "y": 0
                        }
                    ]
                }
            ]    
        }

        return [indicesToLocations, heatmapFormatted.reverse()]
    }
}

export { CalculatedStats }