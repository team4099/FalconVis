/** Class representing an individual point of a statistical criteria. */
class Factor{
    /**
     * Create a point.
     * @callback formula - Anonymous function to get statistical data based on team
     * @param {number} bias - Multiplier on a factor internally to possible modify data to convert to score or other metric
     */
    constructor(formula, bias = 1){
        this.formula = formula
        this.bias = bias
    }

    /**
     * Get the f(team)*bias.
     * @param {number} team - Team number to be passed into formula (callback)
     * @return {number} Return f(team) value with modification by bias
     */
    getValue(team){
        return this.formula(team) * this.bias
    }
}

export { Factor }