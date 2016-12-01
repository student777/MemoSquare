from django import template
import re

register = template.Library()


@register.filter
def to_plain(value):
    value = re.sub(r'</p>|</?br>', '\n', value)
    value = re.sub(r'<.*?>', '', value)
    from html import unescape
    return unescape(value)