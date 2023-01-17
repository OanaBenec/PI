const data = document.currentScript.dataset;
const server_data = data.data;

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

function viewLesson(id) {
    window.location = generateUrl("/main/" + server_data + "/courses/view",
        {
            id: id
        }
    );
}