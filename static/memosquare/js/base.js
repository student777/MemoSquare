/* memo_detail.js */
function edit_memo(pk){
    var url = '/memo/' + pk + '/';
    var settings = {
        method: 'POST',
        data: {
            "title": $("#title").val(),
            "content": $("textarea[name=content]").val(),
            "is_private": $('#fucking_switch').prop('checked'),
            "csrfmiddlewaretoken": csrf_token,
        },
        success: function (response) {
            console.log(response);
            //TODO: response at views_memo is memo object...
            location.href = '/memo/'+pk+'/';
        },
        error: function (response) {
            console.log(response);
        }
    }
    $.ajax(url, settings);
}
function clip_memo(pk, to_clip, caller) {
    var url = '/memo/' + pk + '/clip/';
    var settings = {
        success: function success(result, status, xhr) {
            return;
        },
        error: function (response) {
            console.log(response);
        }
    };

    if (to_clip == true) {
        settings.method = 'POST';
        settings.data = {"csrfmiddlewaretoken": csrf_token};
        settings.success = function(){
            $(caller).text('turned_in');
            var new_onclick = $(caller).attr('onClick').replace("true", "false");
            $(caller).attr('onClick', new_onclick);
        };

    }
    else if (to_clip == false) {
        settings.method = 'DELETE';
        settings.beforeSend = function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        };
        settings.success = function(){
            $(caller).text('turned_in_not');
            var new_onclick = $(caller).attr('onClick').replace("false", "true");
            $(caller).attr('onClick', new_onclick);
        };
    }
    $.ajax(url, settings);
}
function lock_memo(pk, caller){
    var url = '/memo/' + pk + '/lock/';
    var settings = {
        method: 'POST',
        data: {"csrfmiddlewaretoken": csrf_token},
        success: function success(result, status, xhr) {
            var lock = $(caller).text();
            if(lock=='lock_open'){
                lock = 'lock_outline';
            }
            else if(lock=='lock_outline'){
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

// reference: http://ngee.tistory.com/846
function delete_memo(pk) {
    var is_delete = confirm('삭제하시겠습니까?');
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


/* report page */
function open_report(){
    window.open("/report/", "", "width=500,height=400");
}

/* account */
// Send token to our server, server make a session
function sendToken(token) {
    var url = '/sign_in/';
    var settings = {
        method: 'POST',
        data: {'token': token},
        success: function success(result, status, xhr) {
            console.log(result);
            location.href = '/memo/';     // No materials in root page for auth_users
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    };
    $.ajax(url, settings);
}