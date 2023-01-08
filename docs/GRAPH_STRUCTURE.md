# Understanding Graph Structures 📊

## Breakdown of Graphing Structure 

 > 💡 More wrappers, the better

The core of every graph is three things. The Human Layer, Editing Processing Layer, and Drawing Layer.

### Drawing Layer
 - `Graph` Class
    - Essentially a wrapper for ApexCharts Wrapper that takes in individual components like the chart type, colors, data and more and puts it into a json object and then tells apex chart to graph it. It also handles other stuff like updating the graph when new data is given to the class
 -  `ApexCharts` (External Module)
     - The engine and visual generation engine of the graph system. Draws the charts based on the states and data inside the the Graph Class.
 -  Website
     - Contains a container (div) where the graphs will be located and drawn at. This is one of the two parts of human generation but is considered part of the Drawing Layer because of the amount of linkages into `Graph` Class and `ApexCharts`

### Edit Processing Layer
 - `GraphType` Class
     - Takes in data like what teams can be graphed (via JSON) and handles all of the logic for making the modal and what teams are selected on there. It also processes the data and can take in a x value (e.g. team) and call a function to get its data (e.g. avr driver rating) and send that to the Graph Class. There is a GraphType Class for
        - Bar Charts
        - Pie Charts
        - Scatter Plots
        - Line Charts

        ```
        new GraphType(unwrapped_json_data)
        ```
- `CalculatedStats` Class
    - Take in a x and then based on the function will return the y based on the use case. You have to pass in json data from FalconScout

        ```
        var stats = new CalculatedStats(data)
        stats.getStat(team_number, STAT_TYPE)
        ```

- `Modal` Class
    - Modal handles all of the passthrough of data when a graph is changed. This removes chances of entanglement of graphs when they are edited.

### Human Layer
 - JSON
    Consists of the metadata of a graph like location, data formulas, x-axis options, title, and specific customization. Example of a graph JSON is below

    ```
    {
        parent_id: "graphContainer,
        title: "Shooting by match by team",
        plotOptions: {
            bar: {
                horizontal: false
            }
        },
        dataOptions: {
            formulas: {
                "Auto Upper": function(team) {return stats.getAvgStat(team, Queries.AUTO_UPPER_HUB)},
                "Teleop Upper": function(team) {return stats.getAvgStat(team, Queries.TELEOP_UPPER_HUB)}
            },
            selectedOptions: [4099, 118, 180],
            allOptions: Selections.TEAMS
        }
    }
    ```


![Graph Flow](/docs/graph_structure.png)