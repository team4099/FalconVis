class StatMacro {
    constructor(team, parent_id, stat, threshold){
        this.id = Math.random().toString(36).substr(2, 9)

        document.getElementById(parent_id).innerHTML += `
        <div id="${this.id}" class="p-4 border-[1.5px] border-gray-200 rounded-lg h-20" style="width: 400px;">
            <h1 class="mt-1 inline float-left ml-2 font-semibold text-2xl">
                ${stat.name}
            </h1>
            <h1 class="inline float-right mr-4 mt-1 font-bold text-3xl" id="${this.id + "_value"}">
                
            </h1>
        </div>
        `

        this.formula = stat.formula
        
        this.threshold = threshold
        this.team = team
        
    }
    set team(newTeam){
        var result = 0
        result = this.formula(newTeam)

        document.getElementById(this.id + "_value").innerHTML = result.toString()
        if (result < this.threshold){
            document.getElementById(this.id + "_value").style.color = "#ff4a4a"
        }
        else if (result > this.threshold){
            document.getElementById(this.id + "_value").style.color = "#248e24"
        }
        else {
            document.getElementById(this.id + "_value").style.color = "#000000"
        }
    }
}

export { StatMacro }