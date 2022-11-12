class AutomatedMacro {
    constructor(parent_id, title, stat, selectedOptions){
        this.id = Math.random().toString(36).substr(2, 9)

        document.getElementById(parent_id).innerHTML += `
        <div id="${this.id}" class="p-4 border-2 border-gray-200 rounded-lg" style="width: 400px;">
            <h1 class="mt-1 inline float-left ml-2 font-semibold text-2xl">
                ${title}
            </h1>
            <div id="${this.id+"_value"}">
            </div>
        </div>
        `

        this.stat = stat
        
        this.selectedOptions = selectedOptions
        this.pushEdit(this.selectedOptions)
    }

    pushEdit(newTeams){
        this.selectedOptions = newTeams
        console.log(this.selectedOptions)

        document.getElementById(this.id+"_value").innerHTML = "";

        for (const team of this.selectedOptions){
            var result = this.stat.getValue(team)

            if (result[1]){
                var color = "#248e24"
            }
            else {
                var color = "#ff4a4a"
            }

            document.getElementById(this.id+"_value").innerHTML += `
                <div id="${this.id+team.toString()}" class="w-full h-10 mt-4">
                    <h1 class="mt-1 inline float-left ml-2 font-semibold text-2xl">
                        ${team}
                    </h1>
                    <h1 class="mt-1 inline ml-2 font-semibold text-xl" style='float: right; color: ${color}'>
                        ${result[0]}
                    </h1>
                </div>
            `
        }
    }
}

export { AutomatedMacro }