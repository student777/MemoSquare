from .models import Page, Memo, Category
from django.db.models import Q


# Get page or Create Page
# Used when /memo/ POST request
def get_or_create_page(url):
    # Ignore parameters like '#', only treats proper URI data
    # Treat same thing as same, different things as different
    page = find_page(url)
    if page is None:
        page = Page.objects.create(url=url)

    return page


def get_or_create_category(name, user):
    # Consider empty string as uncategorized
    if name == "":
        return None

    # first find category
    try:
        category = Category.objects.get(name=name, user=user)
        return category
    except Category.DoesNotExist:
        category = Category.objects.create(name=name, user=user)

    return category


# find memo list of specific url
# Used when /memo/page?url={url}
def find_memo(url, request):
    page = find_page(url)
    if page is None:
        return

    return Memo.objects.filter(page=page).filter(Q(is_private=False) | Q(user=request.user)).order_by('-pk')


def find_page(url):
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
        return page
    except Page.DoesNotExist:
        pass

    try:
        page = Page.objects.get(url=url_trans)
        return page
    except Page.DoesNotExist:
        pass
