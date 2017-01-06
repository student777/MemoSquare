from xml.etree import ElementTree
import urllib.request
from uuid import uuid4
from django.utils import timezone
from MemoSquare.settings import MEDIA_ROOT, MEDIA_URL
from xml.etree.ElementTree import ParseError
import os


def catch_src(content):
    content_html = ElementTree.fromstring(content)
    src_list = []
    for item in content_html.findall('.//img'):
        src_list.append(item.attrib['src'])
    return src_list


# Not create Memo_image foreign key, just stack images
def save_image(src):
    extension = os.path.splitext(src)[-1].lower()
    random_name = uuid4().hex
    img_path = timezone.now().strftime('/%y/%m/%d/') + random_name + extension
    path_to_save = MEDIA_ROOT + img_path
    # normpath(): independent path by OS
    # directory existence check every request...?
    os.makedirs(os.path.dirname(os.path.normpath(path_to_save)), exist_ok=True)
    # Need to async..?
    urllib.request.urlretrieve(src, path_to_save)
    src_new = MEDIA_URL[0:-1] + img_path
    return src_new


def catch_save(content):
    # content should be parsed perfectly. Need to use regular expression instead of using xml library
    try:
        src_list = catch_src(content)
    except ParseError:
        return content

    replace_table = []
    for src in src_list:
        src_new = save_image(src)
        replace_table.append((src, src_new))

    # Assume that there is no duplicated img src
    for src, src_new in replace_table:
        content = content.replace(src, src_new)

    return content
