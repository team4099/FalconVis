class Graph {
    constructor(id, state) {
        const ApexCharts = window.ApexCharts;

        this.id = id
        this.state = state

        this.state.colors = [
            "#33ca7f",
            "#2bd9fe",
            "#fbbb00",
            "#ff6663",
            "#A03E99",
        ]

        this.graph = new ApexCharts(
            document.getElementById(id),
            this.state
        );

        this.graph.render()

        this.oldState = {
            keys: [],
            values: []
        }

        self = this
        this.anonCheck = function () {self.checkChange()}

        //setInterval(this.anonCheck, 100)
    }

    checkChange() {
        var stateKeys = Object.keys(this.state);
        var stateValues = Object.values(this.state);

        if (!( JSON.stringify(this.oldState.keys) == JSON.stringify(stateKeys) && JSON.stringify(this.oldState.values) == JSON.stringify(stateValues))){
            this.graph.updateOptions(this.state)
            console.log("this")
        }

        this.oldState.keys = Object.keys(this.state)
        this.oldState.values = Object.values(this.state)
    }

    update() {
        this.graph.updateOptions(this.state)
    }



}

export { Graph }