const data = document.currentScript.dataset;
const server_data = JSON.parse(data.data);

console.log(server_data);

function generateUrl(url, params) {
    var i = 0, key;
    for (key in params) {
        if (i === 0) {
            url += "?";
        } else {
            url += "&";
        }
        url += key;
        url += '=';
        url += params[key];
        i++;
    }
    return url;
}

function deleteLesson(index) {
    server_data["lessonsData"].splice(index, 1);
    server_data["lessons"]--;

    for(var i = index; i < server_data["lessonsData"].length; i++) {
        var json = JSON.parse(server_data["lessonsData"][i]);
        json["id"]--;

        var str = JSON.stringify(json);
        server_data["lessonsData"][i] = str;
    }

    console.log(server_data);

    const str2 = JSON.stringify(server_data);
    window.location = generateUrl("/main/" + server_data["name"] + "/courses/add",
        {
            context: str2
        }
    );
}

function editLesson(index) {
    const str2 = JSON.stringify(server_data);
    window.location = generateUrl("/main/" + server_data["name"] + "/courses/add_lesson",
        {
            context: str2,
            edit: index
        }
    );
}

function deleteExercise(index) {
    server_data["exercisesData"].splice(index, 1);
    server_data["exercises"]--;

    for(var i = index; i < server_data["exercisesData"].length; i++) {
        var json = JSON.parse(server_data["exercisesData"][i]);
        json["id"]--;

        var str = JSON.stringify(json);
        server_data["exercisesData"][i] = str;
    }

    console.log(server_data);

    const str2 = JSON.stringify(server_data);
    window.location = generateUrl("/main/" + server_data["name"] + "/courses/add",
        {
            context: str2
        }
    );
}

function editExercise(index) {
    const str2 = JSON.stringify(server_data);
    window.location = generateUrl("/main/" + server_data["name"] + "/courses/add_exercise",
        {
            context: str2,
            edit: index
        }
    );
}

function deleteHomework(index) {
    server_data["homeworksData"].splice(index, 1);
    server_data["homeworks"]--;

    for(var i = index; i < server_data["homeworksData"].length; i++) {
        var json = JSON.parse(server_data["homeworksData"][i]);
        json["id"]--;

        var str = JSON.stringify(json);
        server_data["homeworksData"][i] = str;
    }

    console.log(server_data);

    const str2 = JSON.stringify(server_data);
    window.location = generateUrl("/main/" + server_data["name"] + "/courses/add",
        {
            context: str2
        }
    );
}

function editHomework(index) {
    const str2 = JSON.stringify(server_data);
    window.location = generateUrl("/main/" + server_data["name"] + "/courses/add_homework",
        {
            context: str2,
            edit: index
        }
    );
}


function add_lesson() {
    const str = JSON.stringify(server_data);

    window.location = generateUrl("/main/" + server_data["name"] + "/courses/add_lesson",
        {
            context: str
        }
    );
}

function add_exercise() {
    const str = JSON.stringify(server_data);

    window.location = generateUrl("/main/" + server_data["name"] + "/courses/add_exercise",
        {
            context: str
        }
    );
}

function add_homework() {
    const str = JSON.stringify(server_data);

    window.location = generateUrl("/main/" + server_data["name"] + "/courses/add_homework",
        {
            context: str
        }
    );
}