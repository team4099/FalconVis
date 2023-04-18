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
            }
            return [match, scored]
        }
        catch (e) {
            console.log(e, this.data[team])
            return [[0], [0]]
        }
    }

    getMatchGridScore(team, section, matchKey) {
        try {
            var totalSum = 0

            if (section == Queries.AUTONOMOUS){
                var type = Queries.AUTO_GRID
                var grid_crit = Queries.AUTO_GRID_SCORE
            }
            else {
                var type = Queries.TELEOP_GRID
                var grid_crit = Queries.TELEOP_GRID_SCORE
            }
            
            for (const x of this.data[team]) { 
                if (x[mandatoryMatchData.MATCH_KEY] != matchKey) {
                    continue
                }

                for (const score of x[type]){
                    totalSum += grid_crit[score[1]]
                }

                if (Number.isNaN(totalSum)){
                    totalSum = 0
                }
            }
            return totalSum
        }
        catch (e) {
            console.log(e, this.data[team])
            return 0
        }
    }

    getNotes(team, stat){
        try {
            var notes = []

            for (const x of this.data[team]){
                if (x[stat] != ""){
                    notes.push(x[stat])
                }
            }

            return notes
        }
        catch (e) {
            console.log(e)
            return []
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

    getCumulativeStat(team, stat){
        try {
            var scored = []

            for (const x of this.data[team]) { 
                if (typeof(x[stat]) == "object"){
                    scored.push(x[stat].length)
                }
                else {
                    scored.push(x[stat])
                }
            }

            return scored
        }
        catch (e) {
            return [0]
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

    getAvrGrid(team, stat, type_of_grid){
        try {
            var count = 0
            var totalSubmissions = 0

            for (const x of this.data[team]) { 
                for (const score of x[type_of_grid]){
                    if (stat == Queries.LEFT){
                        if (["1", "2", "3"].includes(score[0])){
                            count += 1
                        }
                        
                    }
                    else if (stat == Queries.COOP){
                        if (["4", "5", "6"].includes(score[0])){
                            count += 1
                        }
                    }
                    else if (stat == Queries.RIGHT){
                        if (["7", "8", "9"].includes(score[0])){
                            count += 1
                        }
                    }
                    else {
                        count += 1
                    }
                }    
                totalSubmissions += 1
            }

            return (count / totalSubmissions).toFixed(2)
        }
        catch (e) {
            return 0
        }
    }

    getCyclesByMatch(team, type_of_grid){
        try {
            var totalCycles = []

            for (const x of this.data[team]) { 
                var count = 0

                for (const _ of x[type_of_grid]){
                    count += 1
                }

                totalCycles.push(count)
            }

            return totalCycles
        }
        catch (e) {
            return 0
        }
    }

    getAutoModes(team) {
        try {
            var autoPoints = []

            for (const x of this.data[team]) { 
                let matchKey = x[mandatoryMatchData.MATCH_KEY]
                var pointValue = 0

                // Calculate autonomous points
                pointValue += this.getMatchGridScore(team, Queries.AUTONOMOUS, matchKey)

                if (pointValue == 0) {
                    continue
                }

                pointValue += this.getScoreDataCritSingle(team, Queries.MOBILITY, Queries.MOBILITY_POINTAGE, matchKey)
                pointValue += this.getScoreDataCritSingle(team, Queries.AUTO_CHARGING_STATE, Queries.AUTO_CHARGE_STATION_CRIT, matchKey)
                
                var gridScoredIn = Queries.COOP

                if (["1", "2", "3"].includes(x[Queries.AUTO_GRID][0][0])) {
                    gridScoredIn = Queries.LEFT
                }
                else if (["4", "5", "6"].includes(x[Queries.AUTO_GRID][0][0])) {
                    gridScoredIn = Queries.COOP
                }
                else if (["7", "8", "9"].includes(x[Queries.AUTO_GRID][0][0])) {
                    gridScoredIn = Queries.RIGHT
                }

                autoPoints.push([pointValue, gridScoredIn])
            }

            return autoPoints
        }
        catch (e) {
            console.log(e)
            return [[-Infinity, Queries.COOP]]
        }
    }

    getAvrTier(team, stat, type_of_grid){
        try {
            var count = 0
            var totalSubmissions = 0
            for (const x of this.data[team]) { 
                for (const score of x[type_of_grid]){
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
                totalSubmissions += 1
            }
            return (count / totalSubmissions).toFixed(2)
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

    getScoreDataCritSingle(team, stat_comp, stat_crit, matchKey = null){
        try {
            var match = []
            var scored = 0
        
            for (const x of this.data[team]) { 
                if (matchKey != null && x[mandatoryMatchData.MATCH_KEY] != matchKey) {
                    continue
                }
                
                match.push(x[mandatoryMatchData.MATCH_KEY])
                scored += stat_crit[x[stat_comp]]
            }
            return scored / match.length
        }
        catch (e) {
            return 0
        }
    }

    getTypeOfGamePiece(team, type_of_grid) {
        var conesScored = 0
        var cubesScored = 0

        for (const x of this.data[team]) {
            for (const score of x[type_of_grid]) {
                if (score[1] == "L" && score.substring(2) == "cone") {
                    conesScored += 1
                }
                else if (score[1] == "L" && score.substring(2) == "cube") {
                    cubesScored += 1
                }
                else if (["1", "3", "4", "6", "7", "9"].includes(score[0])) {
                    conesScored += 1
                }
                else if (["2", "5", "8"].includes(score[0])) {
                    cubesScored += 1
                }
                else {
                    console.log("Edge case with game piece", score)
                }
            }
        }

        return [conesScored, cubesScored]
    }

    getPointsAddedByMatch(team, withEndgame = false, onlyAuto = false, onlyTeleop = false) {
        var pointsAdded = []
        
        try {
            for (const submission of this.data[team]) {
                let matchKey = submission[mandatoryMatchData.MATCH_KEY]

                var pointValue = 0

                // Score during autonomous
                pointValue += this.getMatchGridScore(team, Queries.AUTONOMOUS, matchKey)
                pointValue += this.getScoreDataCritSingle(team, Queries.MOBILITY, Queries.MOBILITY_POINAGE, matchKey)
                pointValue += this.getScoreDataCritSingle(team, Queries.AUTO_CHARGING_STATE, Queries.AUTO_CHARGE_STATION_CRIT, matchKey)

                if (onlyAuto) {
                    pointsAdded.push(pointValue)
                    continue
                }

                // Score during teleop
                let teleopTotal = this.getMatchGridScore(team, Queries.TELEOP, matchKey)
                pointValue += teleopTotal

                if (onlyTeleop) {
                    pointsAdded.push(teleopTotal)
                    continue
                }

                // Score during endgame
                if (withEndgame) {
                    pointValue += this.getScoreDataCritSingle(team, Queries.TOTAL_ENDGAME, Queries.ENDGAME_CRIT, matchKey)
                }
                
                pointsAdded.push(pointValue)
            }

            return pointsAdded.length > 0 ? pointsAdded : [0]
        }
        catch (e) {
            return [0]
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

    calculateCartesianProduct(set1, set2, set3) {
        var cartesianProduct = []

        try {
            for (const x of set1) {
                for (const y of set2) {
                    for (const z of set3) {
                        cartesianProduct.push([x, y, z])
                    }
                }
            }
        }
        catch (e) {
            console.log(e)
            return [[0, 0, 0]]
        }

        return cartesianProduct
    }
    // Calculates the composite stat of an alliance by combining separate lists altogether.
    calculateAllianceCompositeStat(alliance, formula) {
        let allianceCompositeStat = [0, 0, 0].map((_, index) => formula(alliance[index]))
        let cartesianProduct = this.calculateCartesianProduct(...allianceCompositeStat)
        return cartesianProduct.map(
            x => x.reduce((a, b) => a + b)
        )
    }

    optimizeAuto(alliance, sentinel = "qm0") {
        var teamAutos = []
        var bestAutos = []

        for (const team of alliance) {
            teamAutos.push([team, this.getAutoModes(team)])
        }

        teamAutos.sort(
            (a, b) =>  Math.max(...b[1].map(x => x[0])) - Math.max(...a[1].map(x => x[0]))
        )

        teamAutos = teamAutos.map(function(teamModes) {
            const [team, data] = teamModes
            var autoModesAsObject = {
                LEFT_GRID: [],
                COOP_GRID: [],
                RIGHT_GRID: []
            }
            
            for (const [pointage, location] of data) {
                autoModesAsObject[location].push(pointage)
            }

            return [team, Object.entries(autoModesAsObject)]
        })

        let teamAutosAsObject = teamAutos.map(value => [value[0], Object.fromEntries(value[1])])
        let possibleCombinations = this.calculatePermutations([Queries.LEFT, Queries.COOP, Queries.RIGHT])
        
        for (const combination of possibleCombinations) {
            let cumulativeAutoFromCombo = []

            for (let i = 0; i < combination.length; i++) {
                let teamToUse = teamAutosAsObject[i][0]
                let gridData = teamAutosAsObject[i][1]
                let gridToUse = combination[i]

                var maximumPointage = Math.max(...gridData[gridToUse])
                var matchIndex = sentinel // Sentinel value used to denote that there is no auto that works well for said team.

                if (maximumPointage != Number.NEGATIVE_INFINITY) {
                    matchIndex = gridData[gridToUse].indexOf(maximumPointage)
                }
                else {
                    maximumPointage = 0
                }

                cumulativeAutoFromCombo.push([teamToUse, gridToUse, maximumPointage, matchIndex])
            }
            bestAutos.push(cumulativeAutoFromCombo)
        }

        return bestAutos.sort(
            (a, b) => b.map(value => value[2]).reduce((x, y) => x + y) - a.map(value => value[2]).reduce((x, y) => x + y)
        )[0]
    }

    getCycleHeatmapData(team, heatmapGrid, matchKey = null) {
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
                if (matchKey != null && matchData[mandatoryMatchData.MATCH_KEY] != matchKey) {
                    continue
                }

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

    //Credit D3: https://github.com/d3/d3-array/blob/master/LICENSE
    quantileSorted(values, p, fnValueFrom) {
        values.sort((a, b) => a - b)

        var n = values.length
        if (!n) {
            return
        }

        fnValueFrom =
            Object.prototype.toString.call(fnValueFrom) == "[object Function]"
                ? fnValueFrom
                : function (x) {
                    return x
                }

            p = +p

        if (p <= 0 || n < 2) {
            return +fnValueFrom(values[0], 0, values)
        }

        if (p >= 1) {
            return +fnValueFrom(values[n - 1], n - 1, values)
        }

        var i = (n - 1) * p,
        i0 = Math.floor(i),
        value0 = +fnValueFrom(values[i0], i0, values),
        value1 = +fnValueFrom(values[i0 + 1], i0 + 1, values)

        return value0 + (value1 - value0) * (i - i0)
    }

    calculatePermutations(arr) {
        if (!arr.length) {
            return [[]]
        }
        return arr.flatMap(x => {
          // get permutations of arr without x, then prepend x to each
          return this.calculatePermutations(arr.filter(v => v !== x)).map(vs => [x, ...vs]);
        })
    }
}

export { CalculatedStats }