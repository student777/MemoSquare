/* account */
function statusChangeCallback(response) {
    if (response.status === 'connected') {
        // Logged into your app and Facebook.
        console.log('Already logged on');
    } else if (response.status === 'not_authorized') {
        console.log('Please log into this app.');
    } else {
        console.log('Please log into Facebook.');
    }
}
function checkLoginState() {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
}
$(document).ready(function () {
    $.ajaxSetup({cache: true});
    $.getScript('//connect.facebook.net/en_US/sdk.js', function () {
        FB.init({
            appId: '192456264535234',
            cookie: true,
            xfbml: true,
            version: 'v2.5'
        });
        FB.getLoginStatus(function (response) {
            statusChangeCallback(response);
        });
    });
});
// Send FB token to our server, server make a session
function sendToken(token) {
    var url = '/sign_in/';
    var settings = {
        method: 'POST',
        data: {'token': token},
        success: function success(result, status, xhr) {
            console.log(result);
            location.href = '/';
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    };
    $.ajax(url, settings);
}
function signIn() {
    FB.login(function (response) {
        if (response.authResponse) {
            console.log('Welcome!  Fetching your information.... ');
            FB.api('/me', {locale: 'en_US', fields: 'name, email'});
            var token = response.authResponse.accessToken;
            sendToken(token);
        } else {
            console.log('User cancelled login or did not fully authorize.');
        }
    });
}
function signOut() {
    FB.logout(function (response) {
        console.log(response)
    });
    location.href = '/sign_out';
}


/* memo_detail.js */
function edit_memo(pk){
    var url = '/memo/' + pk + '/?format=html';
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
function clip_memo(pk, to_clip) {
    var url = '/memo/' + pk + '/clip/';
    var settings = {
        success: function success(result, status, xhr) {
            location.href = '/memo/'+pk+'/';
        },
        error: function (response) {
            console.log(response);
        }
    }

    if (to_clip == true) {
        settings.method = 'POST';
        settings.data = {"csrfmiddlewaretoken": csrf_token};
    }
    else if (to_clip == false) {
        settings.method = 'DELETE';
        settings.beforeSend = function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
    $.ajax(url, settings);
}

function lock_memo(pk){
    var url = '/memo/' + pk + '/lock/';
    var settings = {
        method: 'POST',
        data: {"csrfmiddlewaretoken": csrf_token},
        success: function success(result, status, xhr) {
            location.href = '/memo/' + pk + '/'
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

function open_report(){
    window.open("/report/", "", "width=500,height=400");
}