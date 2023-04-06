export class NoteHighlighting {
    constructor(parent_id, calc_stat, team, stat, positive_terms, negative_terms){
        this.uuid = Math.random().toString(36).substr(2, 9)

        this.parent_id = parent_id
        this.calc_stat = calc_stat
        this.team = team
        this.stat = stat
        this.positive_terms = positive_terms
        this.negative_terms = negative_terms

        this.companionDiv = document.createElement("div")
        this.companionDiv.classList.add("w-[25rem]", "border-2","border-grey-200", "rounded-md", "pb-0")
        this.companionDiv.id = this.uuid

        document.getElementById(this.parent_id).appendChild(this.companionDiv)

        this.pushEdit(false, team)
    }

    pushEdit(editAll, team) {
        team = parseInt(team[0])
        console.log(team)
        var data = this.calc_stat(team)

        this.companionDiv.innerHTML = `
        <h1 class="ml-4 mt-4 font-semibold text-xl mb-4">Notes - ${this.stat} - ${team}</h1>
        `

        for (var note of data){
            for (const negativeTerm of this.negative_terms){
                note = note.replaceAll(negativeTerm, `<span class="bg-red-200">${negativeTerm}</span>`)
            }

            for (const positiveTerm of this.positive_terms){
                note = note.replaceAll(positiveTerm, `<span class="bg-green-200">${positiveTerm}</span>`)
            }

            this.companionDiv.innerHTML += `
            <div class="px-2 mt-2 pb-2 px-4 border-b border-1 border-grey-400 w-full text-md">
                <h1>${note}</h1>
            </div>
            `
        }
    }
}