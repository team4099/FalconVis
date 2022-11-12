class Factor{
    constructor(formula, bias){
        this.formula = formula
        this.bias = bias
    }

    getValue(team){
        return this.formula(team) * this.bias
    }
}

export { Factor }