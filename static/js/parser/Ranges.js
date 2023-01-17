
class Range {
    constructor() {
        if(this.constructor == Range) {
            throw new Error("Abstract class cannot be instantiated.");
        }
    }

    getValue() {
        throw new Error("Abstract method has not been implemented.");
    }
}

class RealRange extends Range {
    constructor(min, max, minInclusive, maxInclusive, dataRange) {
        super();
        this.min = min;
        this.max = max;
        this.minInclusive = minInclusive;
        this.maxInclusive = maxInclusive;
        this.dataRange = dataRange;
    }

    getValue() {
        if(this.dataRange != null) {
            let index = Math.round(Math.random() * (this.dataRange.length - 1));
        
            return this.dataRange[index];
        }

        let pick = Math.random() * (this.max - this.min) + this.min;

        if(!this.minInclusive) {
            while(pick == this.min) {
                pick = Math.random() * (this.max - this.min) + this.min;
            }
        }

        if(!this.maxInclusive) {
            while(pick == this.max) {
                pick = Math.random() * (this.max - this.min) + this.min;
            }
        }

        return pick;
    }
}

class IntegerRange extends Range {
    constructor(min, max, minInclusive, maxInclusive, dataRange) {
        super();

        this.min = min;
        this.max = max;
        this.minInclusive = minInclusive;
        this.maxInclusive = maxInclusive;
        this.dataRange = dataRange;
    }

    getValue() {
        if(this.dataRange != null) {
            let index = Math.round(Math.random() * (this.dataRange.length - 1));
        
            console.log(index);

            return this.dataRange[index];
        }

        var min = this.min;
        var max = this.max;

        if(!this.minInclusive) {
            min += 1;
        }

        if(!this.maxInclusive) {
            max -= 1;
        }

        let pick = Math.round(Math.random() * (max - min) + min);

        return pick;
    }
}

class CharacterRange extends Range {
    constructor(min, max, minInclusive, maxInclusive, dataRange) {
        super();
        this.min = min.charCodeAt(0);
        this.max = max.charCodeAt(0);
        this.minInclusive = minInclusive;
        this.maxInclusive = maxInclusive;
        this.dataRange = dataRange;
    }

    getValue() {
        if(this.dataRange != null) {
            let index = Math.round(Math.random() * (this.dataRange.length - 1));
        
            return this.dataRange[index];
        }
        
        var min = this.min;
        var max = this.max;

        if(!this.minInclusive) {
           min += 1;
        }

        if(!this.maxInclusive) {
            max -= 1;
        }

        let pick = Math.round(Math.random() * (max - min) + min);

        return String.fromCharCode(pick);
    }
} 

class StringRange extends Range {
    constructor(min, max, minInclusive, maxInclusive, dataRange) {
        super();
        this.min = min;
        this.max = max;
        this.minInclusive = minInclusive;
        this.maxInclusive = maxInclusive;
        this.dataRange = dataRange;
    }

    getValue() {
        if(this.dataRange != null) {
            let index = Math.round(Math.random() * (this.dataRange.length - 1));
        
            return this.dataRange[index];
        }

        var min = this.min;
        var max = this.max;

        if(!this.minInclusive) {
            min += 1;
        }

        if(!this.maxInclusive) {
            max -= 1;
        }

        let pick = Math.round(Math.random() * (max - min) + min);
        let result = "";
        var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

        for (let i = 0; i < pick; i++) {
            result += characters.charAt(Math.floor(Math.random() * characters.length));
        }

        return result;
    }
} 