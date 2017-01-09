function delete_category(pk, caller) {
    if (confirm('really?')) {
        var settings = {
            type: 'DELETE',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function success(result, status, xhr) {
                console.log($(caller).parent().parent());
                $(caller).parent().parent().remove();
            },
            error: function (response) {
                console.log(response);
            }
        };
        var url = '/category/' + pk + '/';
        $.ajax(url, settings);
    }
}

function edit_category(pk, caller){
    var url = '/category/' + pk + '/';
    var name = $(caller).parent().parent().children().children().get(0).value;
    var settings = {
        method: 'POST',
        data: {
            "name": name,
            "csrfmiddlewaretoken": csrf_token
        },
        success: function (response) {
            alert('name changed')
            console.log(response);
        },
        error: function (response) {
            console.log(response);
        }
    };
    $.ajax(url, settings);
}
