/** Criteria with every point in criteria having equal weight */
class CompositeStat{
    /**
     * Create CompositeStat
     * @param {Factor[]} factors - List of Factors in criteria
     * @param {Number} threshold - setting boolean threshold of conditional if team passes criteria 
     */
    constructor(factors, threshold){
        this.factors = factors
        this.threshold = threshold
    }

    /**
     * Calls each factor in this.factors sums up and gets criteria results
     * @param {Number} team - Team for what the criteria is being evaluated for
     * @return {Boolean} - If team passes critera based on threshold
     */
    getValue(team){
        var sum = 0
        for (const factor of this.factors){
            sum += factor.getValue(team)
        }

        try {
            return [sum.toFixed(2), sum.toFixed(2) >= this.threshold]
        }
        catch {
            return [-1, false]
        }
    }
}

export { CompositeStat }