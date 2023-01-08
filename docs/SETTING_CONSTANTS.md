# Setting Constants

> Taken From FalconVis Component Doc

In the `src/lib/data/Constants.js`, there are 4 different constants you can edit.

1. `Queries` is an enum of values you want to query from you data. For example, in FalconScout, if you are gathering upper hub data in teleop, you may have a data value of `Teleop Upper Hub: 10`. In order to reduce errors in FalconVis, we use enums so that you can autocomplete a dictionary value and not have spelling mistakes in your strings. There are two different formats for how you can setup a query
 - `One to One` is a way to set an enum for a single data value like ` TELEOP_UPPER_HUB: "Teleop Upper Hub"`
 - `One to MANY` is used in order to set a group for generating point values by giving the factors in a point value and their corresping values.
 ```javascript
 TELEOP_TOTAL: {
    "Teleop Lower Hub": 1, 
    "Teleop Upper Hub": 2
}
 ```
2. `Selections` is a way to set identifying data. We generally use these to set options for graphs and macros. We have a few pre-setup for IRI2022 and should be changed for your game. When we say `Selections.RED`, we are using it for getting the alliance type

3. `mandatoryMatchData` is the name of used entry values. If that is not correct, your data will not load. In 4099's data, in FalconScout, we use team_number as our id. **YOU MUST HAVE A VALUE FOR ALL OF THEM**

4. `JSONData` is the link to the hosted JSON data. If the data is local, you may be able to add the path in.