class PriorityStat{
    constructor(factors){
        this.factors = factors
    }
    getValue(team){
        for (const factor of this.factors){
            if (factor.condition(factor.formula.getValue(team))){
                return true
            }
        }
        return false
    }
}