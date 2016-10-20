import json
import urllib
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from oauth2client import client, crypt
from MemoSquare.models import UserDetail


class GoogleTokenBackend(ModelBackend):

    # Override
    def authenticate(self, token=None):
        if token is None:
            return None
        url = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s' % token
        r = urllib.request.urlopen(url)
        data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

        # Validate Google ID tokens
        client_id = data['aud']
        android_client_id = '845247378443-93gq15ivccm26vjfui4b8atmiut6qqsu.apps.googleusercontent.com'
        ios_client_id = '845247378443-7l8gl7re1mtobbi7tm7h08i9vn98jite.apps.googleusercontent.com'
        web_client_id = "845247378443-ra1842br5nqfau9d455ue1re17dpt4io.apps.googleusercontent.com"
        data_verified = client.verify_id_token(token, client_id)

        # If multiple clients access the backend server:
        if data_verified['aud'] not in [android_client_id, ios_client_id, web_client_id]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if data_verified['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
            # if data_verified['hd'] != APPS_DOMAIN_NAME:
            #    raise crypt.AppIdentityError("Wrong hosted domain.")

        code = data_verified['sub']
        try:
            user_detail = UserDetail.objects.get(code=code)
            user = user_detail.user
        except UserDetail.DoesNotExist:
            username = data_verified['name']
            email = data_verified['email']
            user = User.objects.create_user(username=username, email=email)
            UserDetail.objects.create(user=user, provider='google', code=code)
        return user
