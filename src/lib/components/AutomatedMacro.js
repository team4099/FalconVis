class AutomatedMacro {
    constructor(parent_id, title, stat, selectedOptions){
        this.id = Math.random().toString(36).substr(2, 9)

        document.getElementById(parent_id).innerHTML += `
        <div id="${this.id}" class="p-4 border-2 border-gray-200 rounded-lg" style="width: 400px;">
            <h1 class="h-4 w-full mb-4 mt-1 inline float-left ml-2 font-semibold text-2xl">
                ${title}
            </h1>
            <div id="${this.id+"_value"}">
            </div>
        </div>
        `

        this.stat = stat
        
        this.selectedOptions = selectedOptions
        this.pushEdit(false, this.selectedOptions)
    }

    pushEdit(modal, newTeams){
        this.selectedOptions = newTeams

        document.getElementById(this.id+"_value").innerHTML = "";

        console.log(this.selectedOptions)
        for (const team of this.selectedOptions){
            var result = this.stat.getValue(team)
            console.log(result)

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