from .models import Page, Memo


# Get page or Create Page
def classify_url(url):
    # Ignore parameters like '#', only treats proper URI data
    # Treat same thing as same, different things as different
    try:
        page = Page.objects.get(url=url)
    except Page.DoesNotExist:
        page = Page.objects.create(url=url)
    return page


# find memo list of specific url
def find_memo(url):
    try:
        page = Page.objects.get(url=url)
    except Page.DoesNotExist:
        return

    return Memo.objects.filter(page=page)
