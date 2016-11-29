import json
import urllib
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from oauth2client import client, crypt
from MemoSquare.models import UserDetail


class FacebookTokenBackend(ModelBackend):
    def authenticate(self, token=None):
        if token is None:
            return None
        url_debug = 'https://graph.facebook.com/debug_token?input_token=%s&access_token=%s'
        data_debug = get_json_from_facebook(url_debug, token)

        # exit condition to google
        try:
            user_id = data_debug['data']['user_id']
        except KeyError:
            return None

        url_info = 'https://graph.facebook.com/v2.8/%s?access_token=%s&fields=email,name'
        data_info = get_json_from_facebook(url_info, user_id)

        try:
            user_detail = UserDetail.objects.get(code=user_id)
            user = user_detail.user

        # If not exists, create user
        except UserDetail.DoesNotExist:
            username = data_info['name']
            # http://stackoverflow.com/questions/16630972/facebook-graph-api-wont-return-email-address
            if 'email' in data_info:
                email = data_info['email']
            else:
                email = '%s@facebook.com' % username
            user = User.objects.create_user(username=username, email=email)
            UserDetail.objects.create(user=user, code=user_id, provider='facebook')

        return user


def get_json_from_facebook(url, code):
    access_token = '192456264535234|qblTXSc_roZOfMxm96XMmWpP6YI'
    r = urllib.request.urlopen(url % (code, access_token))
    data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    return data


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
        android_client_id = '12130227580-hbc5uqia8venaj64ar4ne3nedgoibbuv.apps.googleusercontent.com'
        web_client_id = "12130227580-iq5bv8mnu8dcv88c1luuimt6dmlgqk1u.apps.googleusercontent.com"
        data_verified = client.verify_id_token(token, client_id)

        # If multiple clients access the backend server:
        if data_verified['aud'] not in [android_client_id, web_client_id]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if data_verified['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
            # if data_verified['hd'] != APPS_DOMAIN_NAME:
            #    raise crypt.AppIdentityError("Wrong hosted domain.")

        #TODO: set picture
        print(data_verified['picture'])
        print(data_verified)

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


