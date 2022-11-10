class Factor{
    constructor(formula, type, bias){
        this.formula = formula
        this.type = type
        this.bias = bias
    }

    get(){
        return this.formula() * bias
    }
}