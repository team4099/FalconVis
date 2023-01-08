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
    }

    update() {
        this.graph.updateOptions(this.state)
    }



}

export { Graph }