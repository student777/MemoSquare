function add_comment(pk) {
    var content = $('input#comment_form').val();
    $.ajax({
        url: '/comment/',
        method: "POST",
        data: {memo: pk, content: content},
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        },
        success: function (response) {
            $('#comment_list').find('tbody').append(response.owner + response.content + response.timestamp + '귀찮아서태그안먹임');
            // increase num_likes of memo
            var num_likes = parseInt($('#num_comments').text());
            console.log(num_likes);
            $('#num_comments').text(++num_likes)
        },
        error: function (response) {
            console.log(response)
        }
    })
}

function edit_comment(pk, caller) {
    var td = $(caller).parent().parent().children().eq(1);
    var content_original = td.text();
    var content_changed = prompt("edit comment", content_original);
    $.ajax({
        url: '/comment/' + pk + '/',
        method: "POST",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        },
        data: {content: content_changed},
        success: function (response) {
            td.text(response.content);
        },
        error: function (response) {
            console.log(response)
        }
    })
}

function delete_comment(pk, caller) {
    var is_delete = confirm('really?');
    if (!is_delete) {
        return false;
    }
    $.ajax({
        url: '/comment/' + pk + '/',
        method: "DELETE",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        },
        success: function (response) {
            $(caller).parent().parent().remove();
            $('#comment' + pk).remove();
            // dedcrease num_likes of memo
            var num_likes = parseInt($('#num_comments').text());
            $('#num_comments').text(--num_likes)
        },
        error: function (response) {
            console.log(response)
        }
    })
}

function like_comment(pk, caller) {
    $.ajax({
        url: '/comment/' + pk + '/like/',
        method: "POST",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        },
        success: function (response) {
            var tr = $(caller).parent().parent();
            var num_likes = parseInt(tr.find("#num_likes").text());
            tr.find("#num_likes").text(++num_likes);
            tr.find("#is_liked").show();
            tr.find("#is_not_liked").hide();
        },
        error: function (response) {
            alert(response.responseText);
        }
    })
}

function dislike_comment(pk, caller) {
    $.ajax({
        url: '/comment/' + pk + '/like/',
        method: "DELETE",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        },
        success: function (response) {
            var tr = $(caller).parent().parent();
            var num_likes = parseInt(tr.find("#num_likes").text());
            tr.find("#num_likes").text(--num_likes);
            tr.find("#is_liked").hide();
            tr.find("#is_not_liked").show();
        },
        error: function (response) {
            alert(response.responseText);
        }
    })
}
