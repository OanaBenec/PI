const data = document.currentScript.dataset;
const code = document.getElementById("code-editor");
const server_data = data.data;

// init pyodide and show sys.version when it's loaded successfully
async function main() {
    let pyodide = await loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.20.0/full/",
    });
    return pyodide;
  }
  
  // run the main function
  let pyodideReadyPromise = main();
  
  // pass the editor value to the pyodide.runPython function and show the result in the output section
  async function evaluatePython() {
    let pyodide = await pyodideReadyPromise;
    try {
        document.getElementById("title").innerHTML = "Running Tests... please wait";
        
        var output = [];
        await fetch('/tests/generateOutput/' + server_data, {method: 'GET', 
            headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        }})
            .then((response) => response.json())
            .then((data) => output = data["testCases"]);
        console.log(output);
        
        let results = [];
        for(let i = 0; i < output.length; i++) {
            var input = output[i]["input"];
            var Poutput = output[i]["output"];

            var keys = Object.keys(input);    
            for(var j = 0; j < keys.length; j++) {
                pyodide.globals.set(keys[j], input[keys[j]]);
            }

            let res = pyodide.runPython(code.value);
            let correct = true;

            keys = Object.keys(Poutput); 
            for(var j = 0; j < keys.length; j++) {
                if(Poutput[keys[j]] != pyodide.globals.get(keys[j])) {
                    correct = false;
                    break;
                }
            }
            results.push(correct);
        }

        let noTrue = 0;
        let noFalse = 0;
        for(let i = 0; i < results.length; i++) {
            if(results[i])
                noTrue++;
            else
                noFalse++;
        }

        const title = document.getElementById("title");
        title.innerHTML = "[" + noTrue + " passed / " + noFalse + " failed]";

        document.getElementById("clearable").innerHTML = "<div id=\"results\"> </div>"; 
        const resultsArea = document.getElementById("results");
        
        for(let rows = 0; rows < results.length / 2; rows++) {
            var div = document.createElement('div');
            div.className = "row";
            div.id = "results" + rows;

            resultsArea.insertAdjacentElement('beforebegin', div);
            
            const row = document.getElementById("results" + rows);
            for(let index = 0; index < 2; index++) {
                row.innerHTML += '<div class="col-6" id="div' + index + '_' + rows + '"></div>';

                const sub = document.getElementById("div" + index + "_" + rows);
                if(results[2 * rows + index]) {
                    sub.innerHTML += '<div class="card csuccess" type="button" id="sub2_' + rows +'_' + index +'"></div>';
                }
                else {
                    sub.innerHTML += '<div class="card cdanger" type="button" id="sub2_' + rows +'_' + index +'"></div>';
                }
                const sub2 = document.getElementById("sub2_" + rows + '_' + index);

                sub2.innerHTML += '<div class="row" id="sub3_' + rows +'_' + index +'"></div>';
                document.getElementById("sub3_" + rows + '_' + index).innerHTML += '<div class="col-3" id="sub4_' + rows +'_' + index +'"></div>';
                document.getElementById("sub4_" + rows + '_' + index).innerHTML += '<h2 class="card-title">Test ' + (rows * 2 + index + 1) + '</h2>';

                if(results[2 * rows + index]) {
                    document.getElementById("sub4_" + rows + '_' + index).innerHTML += '<hr class="green line" style="height: 3px;">';
                    document.getElementById("sub4_" + rows + '_' + index).innerHTML += '<p class="card-text">Well done!</p>';
                }
                else {
                    document.getElementById("sub4_" + rows + '_' + index).innerHTML += '<hr class="red line" style="height: 3px;">';
                    document.getElementById("sub4_" + rows + '_' + index).innerHTML += '<p class="card-text">Failed!</p>';
                }

                document.getElementById("sub3_" + rows + '_' + index).innerHTML += '<div class="col-8" id="sub5_' + rows + '_' + index +'"></div>';
                
                const sub5 = document.getElementById("sub5_" + rows + '_' + index);
                if(results[2 * rows + index]) {
                    sub5.innerHTML += '<i class="bi bi-check-circle-fill icon-test check">';
                }
                else {
                    sub5.innerHTML += '<i class="bi bi-x-circle-fill icon-test fail">'
                }

            }
        }

    } catch (err) {
      console.log(err);
    }
  }