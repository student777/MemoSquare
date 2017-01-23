function add_comment(pk) {
    var content = $('input#comment_form').val();
    $.ajax({
        url: '/comment/?format=html',
        method: "POST",
        data: {memo_pk: pk, content: content},
        success: function (response) {
            console.log(response);
            $('#comment_list').append(response);
            // increase num_likes of memo
            var num_likes = parseInt($('#num_comments').text());
            $('#num_comments').text(++num_likes);
        },
        error: function (response) {
            console.log(response)
        }
    })
}

function comment_form(pk, content_original) {
    var comment_modal = $('#edit-comment-modal');
    comment_modal.modal('open');
    comment_modal.find('#comment_content').val(content_original);
    comment_modal.find('#comment_pk').val(pk);
}

function edit_comment(caller) {
    var div = $(caller).parent().parent();
    var pk = div.find('input#comment_pk').val()
    var content = div.find('input#comment_content').val();
    $.ajax({
        url: '/comment/' + pk + '/',
        method: "POST",
        data: {content: content},
        success: function (response) {
            $('#edit-comment-modal').modal('close');
            location.href="";
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
