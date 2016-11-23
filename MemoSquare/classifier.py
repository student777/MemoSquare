from .models import Page, Memo
from django.db.models import Q


# Get page or Create Page
def classify_url(url):
    # Ignore parameters like '#', only treats proper URI data
    # Treat same thing as same, different things as different

    # Server doesn't know that if url in DB ends with slash or not, so search both
    if url.endswith('/'):
        url_trans = url[:-1]
    else:
        url_trans = url + '/'

    # If exists('OR' search), get page. Otherwise create page
    # By the way, will page.url stored in DB ends with slash or not? It depends on the request which first came
    # If first request's url ends with slash, that url will be stored in DB and never change although next request's url
    # does not ends with slash..

    try:
        page = Page.objects.get(url=url)
    except Page.DoesNotExist:
        try:
            page = Page.objects.get(url=url_trans)
        except Page.DoesNotExist:
            page = Page.objects.create(url=url)
    return page


# find memo list of specific url
def find_memo(url, request):
    # Server doesn't know that if url in DB ends with slash or not, so search both
    if url.endswith('/'):
        url_trans = url[:-1]
    else:
        url_trans = url + '/'

    try:
        page = Page.objects.get(url=url)
    except Page.DoesNotExist:
        try:
            page = Page.objects.get(url=url_trans)
        except Page.DoesNotExist:
            return

    return Memo.objects.filter(page=page).filter(Q(is_private=False) | Q(owner=request.user))
