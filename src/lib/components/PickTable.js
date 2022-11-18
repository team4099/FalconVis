import { CalculatedStats } from '../data/CalculatedStats.js';
import { Queries, JSONData } from '../data/Constants.js'
class PickTable {
    
    constructor(tableId, data){

        this.stats = new CalculatedStats(data)
        this.teams = []
        this.id = Math.random().toString(36).substr(2, 9)

        for (const team in data) { 
            document.getElementById(tableId).innerHTML += `
        <tr id = "Team${team}" class="bg-white border-b dark:border-gray-700 hover:bg-gray-50 ">
                <td class="py-4 px-6 text-gray-800 font-black">
                    ${this.stats.getFalconRank(team)}
                </td>
                <td class="py-4 px-6 text-gray-800 font-black">
                    ${team}
                </td>
                <td class="py-4 px-6 text-green-500 font-black">
                    ${this.stats.getAvrStat(team, Queries.TELEOP_UPPER_HUB)}
                </td>
                <td class="py-4 px-6 text-red-500 font-black">
                    ${this.stats.getAvrStat(team, Queries.DEFENSE_RATING) }
                </td>
				<td class="py-4 px-6 text-green-500 font-black">
					20
                </td>
                <td class="py-4 px-6">
                    <!-- Modal toggle -->
                    <a href="#" type="button" data-modal-toggle="editUserModal" class="font-medium text-blue-600 dark:text-blue-500 hover:underline"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"></path></svg></a>
                </td>
        </tr>
        `
        this.teams.push(team)
        } 

        this.tableId = tableId  
        
    }
    getTeams(){
        return this.teams
    }

    sortByFalconRank(){
        var tempMet = []
        for(const x of this.teams){
            tempMet.push(this.stats.getFalconRank(x))
        }
        var tempComb = [];
        for(var x of this.teams){
            tempComb.push([x,tempMet[this.teams.indexOf(x)]])
        }
        tempComb.sort(function(a, b){  
            return (a[1] - b[1])
        
          });
        this.teams = tempComb.map(function(value,index) { return value[0]; });
        this.remakeTable();
    }

    sortByMetric(metric){
        var tempMet = []
        for(const x of this.teams){
            tempMet.push(this.stats.getAvrStat(x, metric))
        }
        var tempComb = [];
        for(var x of this.teams){
            tempComb.push([x,tempMet[this.teams.indexOf(x)]])
        }
        tempComb.sort(function(a, b){  
            return (b[1] - a[1])
        
          });
        this.teams = tempComb.map(function(value,index) { return value[0]; });
        this.remakeTable();
    }

    remakeTable(){
        document.getElementById(this.tableId).innerHTML = ''
        for(const team of this.teams){
            document.getElementById(this.tableId).innerHTML += `
            <tr id = "Team${team}" class="bg-white border-b dark:border-gray-700 hover:bg-gray-50 ">
                <td class="py-4 px-6 text-gray-800 font-black">
                    ${this.stats.getFalconRank(team)}
                </td>
                <td class="py-4 px-6 text-gray-800 font-black">
                    ${team}
                </td>
                <td class="py-4 px-6 text-green-500 font-black">
                    ${this.stats.getAvrStat(team, "Teleop Upper Hub")}
                </td>
                <td class="py-4 px-6 text-red-500 font-black">
                    ${this.stats.getAvrStat(team, this.stats.getAvrStat(team, "Defense Rating"))}
                </td>
				<td class="py-4 px-6 text-green-500 font-black">
					20
                </td>
                <td class="py-4 px-6">
                    <!-- Modal toggle -->
                    <a href="#" type="button" data-modal-toggle="editUserModal" class="font-medium text-blue-600 dark:text-blue-500 hover:underline"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"></path></svg></a>
                </td>
            </tr>
            `
        }
    }
}

export { PickTable }