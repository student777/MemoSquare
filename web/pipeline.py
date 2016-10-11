from django.shortcuts import redirect
from social.backends.google import GoogleOAuth2
from social.pipeline.partial import partial
from social.backends.facebook import FacebookOAuth2


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            return redirect('web:index')


def save_profile(backend, user, response, *args, **kwargs):
    if isinstance(backend, GoogleOAuth2):
        if response.get('image') and response['image'].get('url'):
            url = response['image'].get('url')
            user_detail = user.userdetail
            user_detail.img_url = url
            user_detail.save()
    if isinstance(backend, FacebookOAuth2):
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        user_detail = user.userdetail
        user_detail.img_url = url
        user_detail.save()
