import json
import urllib
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from MemoSquare.models import UserDetail


class FacebookTokenBackend(ModelBackend):
    def authenticate(self, token=None):
        if token is None:
            return None
        url_debug = 'https://graph.facebook.com/debug_token?input_token=%s&access_token=%s'
        data_debug = get_json_from_facebook(url_debug, token)
        user_id = data_debug['data']['user_id']

        url_info = 'https://graph.facebook.com/v2.8/%s?access_token=%s&fields=email,name'
        data_info = get_json_from_facebook(url_info, user_id)

        try:
            user_detail = UserDetail.objects.get(code=user_id)
            user = user_detail.user
        except UserDetail.DoesNotExist:
            username = data_info['name']
            email = data_info['email']
            user = User.objects.create_user(username=username, email=email)
            UserDetail.objects.create(user=user, code=user_id)
        return user


def get_json_from_facebook(url, code):
    access_token = '192456264535234|qblTXSc_roZOfMxm96XMmWpP6YI'
    url = url % (code, access_token)
    r = urllib.request.urlopen(url)
    data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    return data



