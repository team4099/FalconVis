class Factor{
    constructor(formula, type){
        this.formula = formula
        this.type = type
    }

    get(){
        return this.formula()
    }
}