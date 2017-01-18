function like_comment(pk, caller) {
    $.ajax({
        url: '/comment/' + pk + '/like/',
        method: "POST",
        data: {csrfmiddlewaretoken: csrf_token},
        success: function (response) {
            var num_likes = parseInt($(caller).parent().parent().children().eq(3).text()) + 1;
            $(caller).parent().parent().children().eq(3).text(num_likes);
        },
        error: function (response) {
            alert(response.responseText);
        }
    })
}

function dislike_comment(pk, caller) {
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
            var num_likes = parseInt($(caller).parent().parent().children().eq(3).text()) - 1;
            $(caller).parent().parent().children().eq(3).text(num_likes);
        },
        error: function (response) {
            alert(response.responseText);
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
            // increase num_likes of memo
            var num_likes = parseInt($('#num_comments').text()) + 1;
            $('#num_comments').text(num_likes + ' comments')
        },
        error: function (response) {
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
        },
        error: function (response) {
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
            // dedcrease num_likes of memo
            var num_likes = parseInt($('#num_comments').text()) - 1;
            $('#num_comments').text(num_likes + ' likes')
        },
        error: function (response) {
            console.log(response)
        }
    })
}


