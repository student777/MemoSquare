/* report page */
function open_report() {
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