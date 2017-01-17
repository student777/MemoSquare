function like_comment(pk) {
    $.ajax({
        'url': '/comment/' + pk + '/like/',
        "method": "POST",
        'data': {"csrfmiddlewaretoken": csrf_token},
        "success": function (response) {
            console.log(response)
        }
    })
}

function dislike_comment(pk) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    });
    $.ajax({
        'url': '/comment/' + pk + '/like/',
        "method": "DELETE",
        'data': {"csrfmiddlewaretoken": csrf_token},
        "success": function (response) {
            console.log(response)
        }
    })
}