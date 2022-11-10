class CompositeStat{
    constructor(factors, threshold){
        this.factors = factors
        this.threshold = threshold
    }
    getValues(){
        sum = 0
        for (const factor in this.factors){
            sum += factor.get()
        }

        return sum >= this.threshold
    }
}