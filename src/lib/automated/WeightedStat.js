class WeightedStat{
    constructor(factors, threshold){
        this.factors = factors
        this.threshold = threshold
    }
    getValue(team){
        var sum = 0
        var values = 0
        for (const factor of this.factors){
            sum += (factor.formula).getValue(team) * factor.weight
            values += factor.weight
            console.log(sum)
        }

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