from .models import Page


def classify_url(url):
    # TODO: parse an URI
    # Ignore parameters like '#'
    try:
        page = Page.objects.get(url=url)
    except Page.DoesNotExist:
        page = Page.objects.create(url=url)
    return page.pk
