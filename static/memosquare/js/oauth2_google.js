/* Google Oauth2 */
function sign_in_google(googleUser) {
    if(is_authenticated) return;  // to prevent redirect loop, give exit condition... FB and google are too diffrent. fucking
    id_token = googleUser.getAuthResponse().id_token;
    sendToken(id_token);
}
function sign_out_google() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        location.href = '/sign_out';
    });
}
