import { Graph } from "./Graph.js"

class LineGraph {
    constructor(parent_id, title, plotOptions, dataOptions, modal, editable = true) {
        this.uuid = Math.random().toString(36).substr(2, 9)

        this.modal = modal

        this.companionDiv = document.createElement("div")
        this.companionDiv.classList.add("p-4", "border-2", "border-gray-200", "rounded-lg")
        this.companionDiv.style.width = "400px"
        this.companionDiv.id = this.uuid

        document.getElementById(parent_id).appendChild(this.companionDiv)

        this.companionDiv = document.getElementById(this.uuid)
        this.companionDiv.setAttribute("type", "button")
        this.companionDiv.setAttribute("data-modal-toggle", this.uuid)

        var self = this
        if (editable) {
            document.getElementById(this.uuid).addEventListener("click", function () {
                self.setupEdit()
                document.getElementById('fakeToggle').click()
            })
        }


        this.formula = dataOptions.formula

        this.selectedColumnOptions = dataOptions.selectedOptions
        this.allColumnOptions = dataOptions.allOptions

        this.generateData()

        this.graph = new Graph(
            this.uuid,
            {
                chart: {
                    type: 'line',
                    zoom: {
                        enabled: false
                    },
                    animations: {
                        enabled: false
                    }
                },
                plotOptions: plotOptions,
                series: this.generatedData,
                xaxis: {
                    type: "category",
                },
                title: {
                    text: title,
                    align: 'left'
                }
            }
        )

    }

    generateData() {
        this.generatedData = []
        for (const teams of this.selectedColumnOptions){
            
            [this.xAxis, this.yAxis] = this.formula(teams)
            this.generatedData.push({
                name: teams.toString(),
                data: this.xAxis.reduce((acc, current, index) => {
                    return [...acc, {x: current, y: this.yAxis[index]}]
                  }, [])
            })
        }


        console.log(this.generatedData)
    }

    setupEdit() {
        var formString = ``

        var self = this
        this.modal.setCallBackClose(function () {
            self.pushEdit()
        })

        for (const i of this.allColumnOptions) {
            if (this.selectedColumnOptions.includes(i)) {
                formString += `
                <div class="flex items-center">
                    <input checked id="${i}${this.uuid}" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/>
                    <label id="for="${i}${this.uuid}" class="ml-2 text-sm font-medium text-gray-300">${i}</label>
                </div>
                `
            }
            else {
                formString += `
                <div class="flex items-center">
                    <input id="${i}${this.uuid}" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/>
                    <label for="${i}${this.uuid}" class="ml-2 text-sm font-medium text-gray-300">${i}</label>
                </div>
                `
            }
        }

        this.modal.formHTML = formString
    }

    pushEdit(modal = true, x = []) {
        if (modal){
            this.selectedColumnOptions = []
            for (const i of this.allColumnOptions) {
                if (document.getElementById(i.toString() + this.uuid.toString()).checked) {
                    this.selectedColumnOptions.push(i)
                }
            }
        }
        else {
            this.selectedColumnOptions = x
        }

        this.generateData()

        this.graph.state.series = this.generatedData

        this.graph.update()
    }
}


export { LineGraph }