$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/category/?format=html",
        xhrFields: {
            withCredentials: true // for authentication
        },
        success: function (response) {
            $('#category-list').append($(response).filter("#response1").html());
            $('#modals').append($(response).filter("#response2").html());
            $('#nav-bar').append($(response).filter("#response3").html());

            // Initialize modal
            $('.modal').modal();

            // Refresh page when category edit/remove modal closed
            $('#category-modal').modal({
                complete: function () {
                    location.href = '';
                }
            });

            // Initialize side mobile nav-bar
            $(".button-collapse").sideNav();

            // Check category radio
            // if category is empty string,  let radio box id="radio" named 'All' memos be checked...?
            $("#radio" + category_id).prop('checked', true);
        },
        error: function (response) {
            console.log(response);
        }
    });
});


// set csrf_token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});