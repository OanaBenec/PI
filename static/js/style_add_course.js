
document.addEventListener("DOMContentLoaded", function(){
    for(var i = 0; i < server_data["lessons"]; i++) {
        var html = document.getElementById("lesson" + i);
        html.style.top = 30 + 10 * i + "%";

        html = document.getElementById("lesson" + i + "_del");
        html.style.top = 28 + 10 * i + "%";

        html = document.getElementById("lesson" + i + "_edit");
        html.style.top = 28 + 10 * i + "%";
    }

    for(var i = 0; i < server_data["exercises"]; i++) {
        var html = document.getElementById("exercise" + i);
        html.style.top = 30 + 10 * i + "%";

        html = document.getElementById("exercise" + i + "_del");
        html.style.top = 28 + 10 * i + "%";

        html = document.getElementById("exercise" + i + "_edit");
        html.style.top = 28 + 10 * i + "%";
    }

    for(var i = 0; i < server_data["homeworks"]; i++) {
        var html = document.getElementById("homework" + i);
        html.style.top = 30 + 10 * i + "%";

        html = document.getElementById("homework" + i + "_del");
        html.style.top = 28 + 10 * i + "%";

        html = document.getElementById("homework" + i + "_edit");
        html.style.top = 28 + 10 * i + "%";
    }
});