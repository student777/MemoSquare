/* memo_detail.js */
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
        settings.success = function () {
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
        settings.success = function () {
            $(caller).text('turned_in_not');
            var new_onclick = $(caller).attr('onClick').replace("false", "true");
            $(caller).attr('onClick', new_onclick);
        };
    }
    $.ajax(url, settings);
}
function lock_memo(pk, caller) {
    var url = '/memo/' + pk + '/lock/';
    var settings = {
        method: 'POST',
        data: {"csrfmiddlewaretoken": csrf_token},
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

// Move new page and pop chrome-extension up
function edit_form(pk) {
    document.dispatchEvent(
        new CustomEvent("loadEditor", {'detail': {'pk': pk}})
    );
}