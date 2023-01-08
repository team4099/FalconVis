# Developing FalconVis Pages

There are three pages for configuration. In this doc, we will explain how it is setup and an example of using the setup. We will not explain graphs or automated components. Refer to the [Component Explanation Guide](./FALCONVIS_COMPONENTS.md)

## Event (src/index.js)

Event is used to show general graphs of teams you want to look at during the overall event. In event, the following is setup for you

 - Data is retrieved from your JSON link in `Constants.json`
 - `CalculatedStats` has been configured and setup with your data and is called **stats**
 - a graph container called `graphContainer` has been added to index.html
 - a `Modal` class has been added with the name **modal**
 - Your constants like `Selections` and `Queries` have been brought in along with every type of Graph

Here is an example of how we generate a graph
```javascript
var driverRating = new BarGraph(
    "graphContainer",
    "Avr Driver Rating by Team",
    {
      bar: {
        horizontal: false
      }
    },
    {
      formula: {
        "Auto Upper": function(team) {return stats.getAvrStat(team, Queries.AUTO_UPPER_HUB)},
        "Teleop Upper": function(team) {return stats.getAvrStat(team, Queries.TELEOP_UPPER_HUB)}
      },
      selectedOptions: [4099, 118, 180],
      allOptions: Selections.TEAMS
    },
    modal
)
```

## Match (src/match/match.js)

Match is used to configure and preview how two teams will stack up in terms of stats by being able to enter three red and three blue teams and view their stats.

 - Pre-generated graph managers for red and blue. When you add a graph to the page, if it is related to red, add it to `graphContainerRed` and if it is blue, add it to `graphContainerBlue`
 - a `Modal` class has been added with the name **modal**
 - Your constants like `Selections` and `Queries` have been brought in along with every type of Graph
 - Data is retrieved from your JSON link in `Constants.json`
 - `CalculatedStats` has been configured and setup with your data and is called **stats**
 - two graph containers called `redAllianceContainer` and `blueAllianceContainer` has been added to match.html
 - Two methods for code organization are setup where you add the graphs for Red and Blue. They are called `generateRedGraphs(stats)` and `generateBlueGraphs(stats)` and are called for you

Example of adding a graph to `graphContainerRed`

```javascript
graphContainerRed.addGraph(
    "teleopCargoRed",
    new BarGraph(
        "redAllianceContainer",
        "Avr. Teleop Cargo - Red",
        {
            bar: {
                horizontal: false
            }
        },
        {
            formulas: {
            "Teleop Lower": function(team) {return stats.getAvrStat(team, Queries.TELEOP_LOWER_HUB)},
            "Teleop Upper": function(team) {return stats.getAvrStat(team, Queries.TELEOP_UPPER_HUB)}
            },
            selectedOptions: red,
            allOptions: Selections.TEAMS
        },
        modal,
        false
    )
)
```

## Team (src/team/team.js)

Team is for viewing macros on team stats like amount of points scored or defense rating by building your own metrics using Composite or Weighted Stat

 - Pre-generated graph managers for the team. When you add a graph or macro to the page, add it to `statManager`. When the user selects a new team, the graph manager will auto update the graphs and macros
 - Your constants like `Selections` and `Queries` have been brought in along with every type of Graph
 - Data is retrieved from your JSON link in `Constants.json`
 - `CalculatedStats` has been configured and setup with your data and is called **stats**
 - a DOM element graph container called `macrosContainer` is made

Make sure to put team as the initial value for teams in the macro. Here is an example of what we are talking about.

```javascript
statManager.addGraph(
    "teleop_upper",
    new AutomatedMacro(
        "macrosContainer", 
        "Avr. Teleop Upper", 
        new CompositeStat(
            [new Factor(function (team) { return stats.getAvrStat(team,Queries.TELEOP_UPPER_HUB)})],
            2
        ),
        team
    )
)
```

