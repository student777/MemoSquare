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


function sign_in_FB() {
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

function sign_out_FB() {
    FB.logout(function (response) {
        console.log(response)
    });
    location.href = '/sign_out';
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


