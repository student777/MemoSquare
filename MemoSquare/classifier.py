from .models import Page, Memo


def classify_url(url):
    # TODO: parse an URI
    # Ignore parameters like '#', only treats proper URI data
    # Treat same thing as same, different things as different
    try:
        page = Page.objects.get(url=url)
    except Page.DoesNotExist:
        page = Page.objects.create(url=url)
    return page


def find_memo(url):
    try:
        page = Page.objects.get(url=url)
    except Page.DoesNotExist:
        return

    return Memo.objects.filter(page=page)
