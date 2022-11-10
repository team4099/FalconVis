class WeightedStat{
    constructor(factors, threshold){
        this.factors = factors
        this.threshold = threshold
    }
    getValues(){
        sum = 0
        values = 0
        for (const factor in this.factors){
            sum += factor[0].get() * factor[1]
        }

        return sum >= this.threshold
    }
}