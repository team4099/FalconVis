import { mandatoryMatchData } from "../data/Constants.js"

class CalculatedStats {
    constructor(data){
        this.old_data = data
        this.data = {}

        for (const entry of this.old_data){
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
                match.push(x[mandatoryMatchData.MATCH_KEY])
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
                match.push(x[mandatoryMatchData.MATCH_KEY])
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
}

export { CalculatedStats }