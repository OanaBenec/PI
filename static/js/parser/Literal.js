
class Literal {
    constructor(identifier, dataType, range) {
        this.ID = identifier;                 
        this.DT = dataType;                   
        this.range = this.getDataRange(range);
    }

    getDataRange(range) {
        var opener = range[0];
        var closer = range[range.length - 1];

        var dataRange = range.substr(1, range.length - 2);
        var dataArr = dataRange.split(/[\s,]+/);

        if(opener === '(' || opener === '[') {
            var limits = [];

            for(var item = 0; item < dataArr.length; item++) {
                limits.push(dataArr[item]);
            }

            if(this.DT == "Integer") {
                return new IntegerRange(parseInt(limits[0]), parseInt(limits[1]), (opener === "["), (closer === "]"), null);
            }
            else if(this.DT == "Real") {
                return new RealRange(parseFloat(limits[0]), parseFloat(limits[1]), (opener === "["), (closer === "]"), null);
            }
            else if(this.DT == "Character") {
                return new CharacterRange(limits[0], limits[1], (opener === "["), (closer === "]"), null);
            }

            return new StringRange(parseInt(limits[0]), parseInt(limits[1]), (opener === "["), (closer === "]"), null);
        }
        else {
            var items = [];

            if(this.DT === "Integer") {
                for(var i = 0; i < dataArr.length; i++) {
                    items.push(parseInt(dataArr[i]));
                }

                return new IntegerRange(0,0,0,0,items);
            }
            else if(this.DT === "Real") {
                for(var i = 0; i < dataArr.length; i++) {
                    items.push(parseFloat(dataArr[i]));
                }

                return new RealRange(0,0,0,0,items);
            }
            else if(this.DT === "Character") {
                return new IntegerRange(0,0,0,0,dataArr);
            }

            return new StringRange(0,0,0,0,dataArr);
        }
    }
}