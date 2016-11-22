from .models import Page, Memo
from django.db.models import Q


# Get page or Create Page
def classify_url(url):
    # Ignore parameters like '#', only treats proper URI data
    # Treat same thing as same, different things as different

    # If exists, get page. Otherwise create page
    try:
        page = Page.objects.get(url=url)
    except Page.DoesNotExist:
        page = Page.objects.create(url=url)
    return page


# find memo list of specific url
def find_memo(url, request):
    # Server don't know that if url in DB ends with slash or not, so execute 'OR' query
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
