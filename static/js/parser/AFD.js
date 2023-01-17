
class FiniteAutomataParser {
    constructor() {
        this.currentState = "ExpectingType";
        this.finalState = "F";
        this.keywords = {
            dataTypes: ["Integer", "Real", "Character", "String"],
            delimiters: {
                openers: ['(', '[', '{'],
                closers: [')', ']']
            }
        };

        this.currentDT = null;
        this.currentLit = null;
        this.currentOpener = null;
        this.currentCloser = null;
        this.currentValues = [];
        this.results = [];
    }

    takeAction(keyword, err) {
        err.innerHTML = "";

        if(this.currentState === "ExpectingType") {
            var found = 0;
            
            if(this.currentDT !== null) {
                err.innerHTML = "Unexpected data type: " + keyword;
                return;
            }
            
            for(var i = 0; i < this.keywords["dataTypes"].length; i++) {
                if(this.keywords["dataTypes"][i] === keyword) {
                    found = 1;
                    this.currentDT = keyword;
                    this.currentState = "ExpectingID";
                    break;
                }
            }

            if(!found) {
                err.innerHTML = "Expecting a data type but got: " + keyword;
            }
        }
        else if(this.currentState === "ExpectingID") {
            if(this.currentLit !== null || keyword === "") {
                err.innerHTML = "Unexpected literal: " + keyword;
                return;
            }

            this.currentLit = keyword;
            this.currentState = "ExpectingOpener";
        }
        else if(this.currentState === "ExpectingOpener") {
            for(var i = 0; i < this.keywords["delimiters"]["openers"].length; i++) {
                if(this.keywords["delimiters"]["openers"][i] === keyword) {
                    found = 1;
                    this.currentOpener = keyword;
                    break;
                }
            }

            if(!found) {
                err.innerHTML = "Expecting a range opener but got: " + keyword;
            }

            if(keyword === "(" || keyword === "[") {
                this.currentState = "ExpectingMinValue";
            }
            else {
                this.currentState = "ExpectingValues";
            }
        }
        else if(this.currentState === "ExpectingMinValue") {
            try {
                this.addValue(keyword);
                this.currentState = "ExpectingMaxValue";
            }
            catch(error) {

            }
        }
        else if(this.currentState === "ExpectingMaxValue") {
            try {
                this.addValue(keyword);
                this.currentState = "ExpectingCloser";
            }
            catch(error) {

            }
        }
        else if(this.currentState === "ExpectingCloser") {
            for(var i = 0; i < this.keywords["delimiters"]["closers"].length; i++) {
                if(this.keywords["delimiters"]["closers"][i] === keyword) {
                    found = 1;
                    this.currentCloser = keyword;
                    break;
                }
            }

            if(!found) {
                err.innerHTML = "Expecting a range closer but got: " + keyword;
                return;
            }

            this.currentState = "F";
            this.saveResults();
        }
        else if(this.currentState === "ExpectingValues") {
            if(keyword === "}") {
                if(this.currentValues.length === 0) {
                    err.innerHTML = "Caught empty interval at: " + keyword;
                    return;
                }

                this.currentState = "F";
                this.currentCloser = "}";
                this.saveResults();
            }
            else {
                try {
                    this.addValue(keyword);
                }
                catch(error) {
    
                }
            }
        }
    }

    getRange() {
        var Srange = this.currentOpener;
        
        for(var i = 0; i < this.currentValues.length; i++) {
            Srange += this.currentValues[i].toString();

            if(i < this.currentValues.length - 1) {
                Srange += ", ";
            }
        }

        Srange += this.currentCloser;
        return Srange;
    }

    clear() {
        this.currentCloser = null;
        this.currentDT = null;
        this.currentLit = null;
        this.currentOpener = null;
        this.currentState = "ExpectingType";
        this.currentValues = [];
    }

    addValue(keyword) {
        try {
            if(keyword === null || keyword.length === 0)
                throw "Expecting " + this.currentDT;

            if(this.currentDT == "Integer") {
                this.currentValues.push(parseInt(keyword));
            }
            else if(this.currentDT == "Integer") {
                this.currentValues.push(parseFloat(keyword));
            }
            else if(this.currentDT == "Character") {
                if(keyword.length > 1)
                    throw "Invalid character: " + keyword;
                this.currentValues.push(keyword);
            }
            else if(this.currentDT == "String") {
                if(this.currentOpener === "(" || this.currentOpener === "[") {
                    this.currentValues.push(parseInt(keyword));
                }
                else {
                    this.currentValues.push(keyword);
                }
            }
        } catch (error) {
            err.innerHTML = error;
            throw 1;
        }
    }

    saveResults() {
        this.results.push(new Literal(this.currentLit, this.currentDT, this.getRange()));
    }

    parseText(text, err) {
        var textArr = text.split(/[\s,\n]+/);

        for(var i = 0; i < textArr.length; i++) {
            if(this.currentState == "F") {
                this.currentState = "ExpectingType";
                this.clear();
            }

            this.takeAction(textArr[i],err);
        }

        if(this.currentState !== "F" && err.innerHTML === "") {
            err.innerHTML = "Incomplete data definition: " + this.currentState;
        }

        var i = this.results;
        this.results = [];

        return i;
    }
}

function myHandler() {
    var afd = new FiniteAutomataParser();
    var txt = document.getElementById("input").value;
    var err = document.getElementById("Error");

    afd.parseText(txt, err);
}