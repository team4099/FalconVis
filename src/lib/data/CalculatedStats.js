class CalculatedStats {
    constructor(data){
        this.data = data
    }

    getFalconRank(team){
        // just so they're diff numbers instead of just 2 :(
        return parseInt(team/2);
    }

    getAvrStat(team, stat){
        try {
            var values = 0
            var count = 0
        
            for (const x of this.data[team]) { 
                values += x[stat]
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
                match.push(x["Match Key"])
                scored.push(temp)
            }
    
            return [match, scored]
        }
        catch (e) {
            return [[0], [0]]
        }
    }

    getScoreData(team, stat){
        try {
            var match = []
            var scored = []
        
            for (const x of this.data[team]) { 
                match.push(x["Match Key"])
                scored.push(x[stat])
            }
    
            return [match, scored]
        }
        catch (e) {
            return [[0], [0]]
        }
    }

    getMatchAllianceData(match, stat, alliance){
        try {
            var teams = []
            var scored = []
        
            for (const x of Object.values(this.data)) { 
                for (const l of x){
                    if (l["Match Key"] == match && l["Alliance"] == alliance){
                        teams.push(l["Team Number"].toString())
                        scored.push(l[stat])
                        break
                    }
                }
            }
    
            return [teams, scored]
        }
        catch (e) {
            return [[0], [0]]
        }
    }
}

export { CalculatedStats }