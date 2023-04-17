class AutomatedMacro {
    constructor(parent_id, title, stat, selectedOptions, largeText = true, appendPercentage = false){
        this.id = Math.random().toString(36).substr(2, 9)

        const temp = document.createElement('div');
        temp.setAttribute("id", parent_id);
        temp.setAttribute("class", "p-4 border-2 border-gray-200 rounded-lg")
        temp.setAttribute("style", "width: 400px;")
        temp.innerHTML = `
        <div class="h-8 w-full mt-1 ml-2 mb-4">
            <h1 class="inline float-left font-semibold text-2xl">
                ${title}
            </h1>
        </div>
        <div class="w-full" id="${this.id+"_value"}">
        </div>
        `

        document.getElementById(parent_id).appendChild(temp)
        
        
        this.stat = stat
        this.largeText = largeText
        this.appendPercentage = appendPercentage
        
        this.selectedOptions = selectedOptions
        this.pushEdit(false, this.selectedOptions)
        
    }

    pushEdit(modal, newTeams){
        this.selectedOptions = newTeams

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
                <div id="${this.id+team.toString()}" class="w-full h-10 mt-2">
                    <h1 class="mt-1 inline float-left ml-2 font-semibold ${this.largeText ? 'text-2xl' : 'text-xl'}">
                        ${team}
                    </h1>
                    <h1 class="mt-1 inline ml-2 font-semibold text-xl" style='float: right; color: ${color}'>
                        ${result[0]}${this.appendPercentage ? '%' : ''}
                    </h1>
                </div>
            `
        }
    }
}

export { AutomatedMacro }