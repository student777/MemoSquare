from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def sign_in(request):
    # TEST
    from oauth2client import client, crypt

    # (Receive token by HTTPS POST)
    token = request.POST.get('idToken')
    # TODO: get and save info about user

    # ???
    CLIENT_ID = '845247378443-ra1842br5nqfau9d455ue1re17dpt4io.apps.googleusercontent.com'
    ANDROID_CLIENT_ID = '845247378443-93gq15ivccm26vjfui4b8atmiut6qqsu.apps.googleusercontent.com'
    IOS_CLIENT_ID = '845247378443-7l8gl7re1mtobbi7tm7h08i9vn98jite.apps.googleusercontent.com'
    WEB_CLIENT_ID = "845247378443-ra1842br5nqfau9d455ue1re17dpt4io.apps.googleusercontent.com"

    # Validate Google ID tokens
    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        # If multiple clients access the backend server:
        if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
        # if idinfo['hd'] != APPS_DOMAIN_NAME:
        #    raise crypt.AppIdentityError("Wrong hosted domain.")
    except crypt.AppIdentityError:
        # Invalid token
        print('invalid token')

    # 무엇에 쓰는 물건인고
    userid = idinfo['sub']
    print(userid, 'userid saved in server')

    return HttpResponse('hello SunYoung mom, I am MoonOld father')


def sign_out(request):
    return HttpResponse('sign_out hello world')
