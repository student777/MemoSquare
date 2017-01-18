// reference: http://ngee.tistory.com/846
function delete_memo(pk) {
    var is_delete = confirm('really?');
    if (!is_delete) {
        return false;
    }
    var settings = {
        type: 'DELETE',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function success(result, status, xhr) {
            //delete <td> is troublesome
            //일단나의메모페에지로
            location.href = '/memo/'
        },
        error: function (response) {
            console.log(response);
        }
    };
    var url = '/memo/' + pk + '/';
    $.ajax(url, settings);
}

// Move new page and pop chrome-extension up
function edit_form(pk) {
    document.dispatchEvent(
        new CustomEvent("loadEditor", {detail: {pk: pk}})
    );
}

 /*
 Compare to 'like & dislike' module, Requirements are same, but implementation is different in 'clip' module.
 Both require 1)POST & DELETE ajax request 2)icon should be changed on each request.
 'clip' module is complex in javascript function, but simple in html
 'like & dislike' module is simple in function logic and signature, but complex in html and using many html 'id' attribute.
 */
function clip_memo(pk, to_clip, caller) {
    var url = '/memo/' + pk + '/clip/';
    var settings = {
        beforeSend : function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        error: function(response) {
            console.log(response);
        }
    };

    // manage num_clip(works only in list_view)
    var parent_div = $(caller).parent().parent();
    var clips_div = parent_div.find('div.clip-text > span');

    if (to_clip == true) {
        settings.method = 'POST';
        settings.success = function () {
            $(caller).text('turned_in');
            var new_onclick = $(caller).attr('onClick').replace("true", "false");
            $(caller).attr('onClick', new_onclick);

            // increase num_clip(works only in list_view)
            var num_clip = parseInt(clips_div.text());
            clips_div.text(++num_clip);
        }
    }
    else if (to_clip == false) {
        settings.method = 'DELETE';
        settings.success = function () {
            $(caller).text('turned_in_not');
            var new_onclick = $(caller).attr('onClick').replace("false", "true");
            $(caller).attr('onClick', new_onclick);

            // decrease num_clip(works nly in list_view)
            var num_clip = parseInt(clips_div.text());
            clips_div.text(--num_clip);

            // remove card (works only in clip_list)
            if(window.location.href.endsWith('/clipbook/')){
                $(caller).parent().parent().parent().parent().parent().remove();
            }
        };
    }

    $.ajax(url, settings);
}

function lock_memo(pk, caller) {
    var url = '/memo/' + pk + '/lock/';
    var settings = {
        method: 'POST',
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        },
        success: function success(result, status, xhr) {
            var lock = $(caller).text();
            if (lock == 'lock_open') {
                lock = 'lock_outline';
            }
            else if (lock == 'lock_outline') {
                lock = 'lock_open';
            }
            $(caller).text(lock);
        },
        error: function (response) {
            console.log(response);
        }
    };
    $.ajax(url, settings);
}

function share_memo() {
    if (typeof memo != undefined) {
        var facebookURL = "https://www.facebook.com/sharer/sharer.php"
            + "?u=http://memo-square.com/memo/" + memo.pk
            + "&title=" + memo.title;
        window.open(facebookURL, "", "width=500,height=400");
    }
}

function like_memo(pk, caller) {
    $.ajax({
        url: '/memo/' + pk + '/like/',
        method: "POST",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        },
        success: function (response) {
            var div = $(caller).parent();
            var num_likes = parseInt(div.find("#num_likes").text());
            div.find("#num_likes").text(++num_likes);
            div.find("#is_liked").show();
            div.find("#is_not_liked").hide()
        },
        error: function (response) {
            alert(response.responseText);
        }
    })
}

function dislike_memo(pk, caller) {
    $.ajax({
        url: '/memo/' + pk + '/like/',
        method: "DELETE",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (response) {
            var div = $(caller).parent();
            var num_likes = parseInt(div.find("#num_likes").text());
            div.find("#num_likes").text(--num_likes);
            div.find("#is_liked").hide();
            div.find("#is_not_liked").show()
        },
        error: function (response) {
            alert(response.responseText);
        }
    })
}