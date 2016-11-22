from .models import Page, Memo
from django.db.models import Q


# Get page or Create Page
def classify_url(url):
    # Ignore parameters like '#', only treats proper URI data
    # Treat same thing as same, different things as different

    # URL must end with slash
    # Because Chrome extension adds slash to URL...
    if not url.endswith('/'):
        url += '/'

    # If exists, get page. Otherwise create page
    try:
        page = Page.objects.get(url=url)
    except Page.DoesNotExist:
        page = Page.objects.create(url=url)
    return page


# find memo list of specific url
def find_memo(url, request):
    try:
        page = Page.objects.get(url=url)
    except Page.DoesNotExist:
        return

    return Memo.objects.filter(page=page).filter(Q(is_private=False) | Q(owner=request.user))
