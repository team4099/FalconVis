class CompositeStat{
    constructor(factors, threshold){
        this.factors = factors
        this.threshold = threshold
        this.bias = bias
    }
    getValue(team){
        var sum = 0
        for (const factor in this.factors){
            sum += factor.getValue(team)
        }

        return sum >= this.threshold
    }
}

export { CompositeStat }