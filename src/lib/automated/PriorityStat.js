/** Criteria with all or nothing points where as long as one point passes in order of priority, criteria is met */
class PriorityStat{
    /**
     * Create PriorityStat
     * @param {Factor[]} factors - List of Factors in criteria [{condition: {Callback}, formula: Factor}]
     */
    constructor(factors){
        this.factors = factors
    }

    /**
     * Sees if team passes priority criteria
     * @param {Number} team - Team to be check against priority criteria
     * @returns {Boolean} - If team passes any one of the criteria points
     */
    getValue(team){
        for (const factor of this.factors){
            // Gets result from Factor and passes to anonymous function to see if it passes condition
            if (factor.condition(factor.formula.getValue(team))){
                return true
            }
        }
        return false
    }
}