// Create class for adding weights to factors in criteria
class WeightedStat{
    /**
     * Create a WeightedStat
     * @param {Factor[]} factors - List of Factors and their corresponding weights in the criteria
     * @param {Number} threshold - Setting boolean threshold of conditional if team passes criteria
     */
    constructor(factors, threshold){
        this.factors = factors
        this.threshold = threshold
    }
    /**
     * Takes team and sees if it passes the criteria
     * @param {Number} team - Team to be fed through the critera
     * @returns {Boolean} - If team passes criteria based on threshold set at init
     */
    getValue(team){
        var sum = 0
        var values = 0

        // Loops through ever factor and sums factor value and weights
        for (const factor of this.factors){
            sum += (factor.formula).getValue(team) * factor.weight
            values += factor.weight
            console.log(sum)
        }


        // Divides the sum and values and compares to threshold. In try catch to avoid math by 0 errors. Todo: Check if needed.
        try {
            console.log(sum, values)
            return [(sum/values).toFixed(2), (sum/values).toFixed(2) >= this.threshold]
        }
        catch {
            return [-1, false]
        }
    }
}

export { WeightedStat }