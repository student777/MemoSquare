function like_comment(pk) {
    $.ajax({
        url: '/comment/' + pk + '/like/',
        method: "POST",
        data: {csrfmiddlewaretoken: csrf_token},
        success: function (response) {
            console.log(response)
        }
    })
}

function dislike_comment(pk) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        }
    });
    $.ajax({
        url: '/comment/' + pk + '/like/',
        method: "DELETE",
        data: {csrfmiddlewaretoken: csrf_token},
        success: function (response) {
            console.log(response)
        }
    })
}

function add_comment(pk){
    var content = $('input#comment').val();
    $.ajax({
        url: '/comment/',
        method: "POST",
        data: {csrfmiddlewaretoken: csrf_token, memo: pk, content: content},
        success: function (response) {
            $('#comment_list').append(response.content);
            console.log(response)
        }
    })
}

function edit_comment(pk){
    var content = prompt("sometext","defaultText");
    $.ajax({
        url: '/comment/' + pk + '/',
        method: "POST",
        data: {csrfmiddlewaretoken: csrf_token, content: content},
        success: function (response) {
            $('#comment' + pk + '> td').eq(1).text(response.content);
            console.log(response)
        }
    })
}


function delete_comment(pk){
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    });
    $.ajax({
        url: '/comment/' + pk + '/',
        method: "DELETE",
        success: function (response) {
            $('#comment'+pk).remove();
            console.log(response);
        }
    })
}


