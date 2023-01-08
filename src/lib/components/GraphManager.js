export class GraphManager{
    constructor(){
        this.graphs = {}
    }

    addGraph(id, graph){
        this.graphs[id] = graph
    }

    pushEditEach(id, values){
        this.graphs[id].pushEdit(false, values)
    }

    pushEditAll(values){
        var graphKeys = Object.values(this.graphs);
        for (const graph of graphKeys){
            graph.pushEdit(false, values)
        }
    }
}