/** Criteria with every point in criteria having equal weight */
class CompositeStat{
    /**
     * Create CompositeStat
     * @param {Factor[]} factors - List of Factors in criteria
     * @param {number} threshold - setting boolean threshold of conditional if team passes criteria 
     */
    constructor(factors, threshold){
        this.factors = factors
        this.threshold = threshold
        this.bias = bias
    }

    /**
     * Calls each factor in this.factors sums up and gets criteria results
     * @param {*} team - Team for what the criteria is being evaluated for
     * @return {boolean} - If team passes critera based on threshold
     */
    getValue(team){
        var sum = 0
        for (const factor in this.factors){
            sum += factor.getValue(team)
        }

        return sum >= this.threshold
    }
}

export { CompositeStat }