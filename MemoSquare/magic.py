from xml.etree import ElementTree
import urllib.request
from django.utils import timezone
from MemoSquare.settings import MEDIA_ROOT, MEDIA_URL
from xml.etree.ElementTree import ParseError
import os
import base64
import uuid
import imghdr


def catch_src(content):
    content_html = ElementTree.fromstring(content)
    src_list = []
    for item in content_html.findall('.//img'):
        src_list.append(item.attrib['src'])
    return src_list


def make_path(file_extension):
    # Generate file name, extension, Get date
    file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
    complete_file_name = "%s.%s" % (file_name, file_extension,)
    path_dated = timezone.now().strftime('/%y/%m/%d/') + complete_file_name
    path_system = MEDIA_ROOT + path_dated

    # Make directory
    os.makedirs(os.path.dirname(os.path.normpath(path_system)), exist_ok=True)
    return path_dated, path_system


# Not create Memo_image foreign key, just stack images
def save_image_src(src):
    extension = os.path.splitext(src)[-1].lower()[1:]
    path_dated, path_system = make_path(extension)
    # Need to async..?
    urllib.request.urlretrieve(src, path_system)
    path_media = MEDIA_URL[0:-1] + path_dated
    return path_media


def catch_save(content):
    # content should be parsed perfectly. Need to use regular expression instead of using xml library
    try:
        src_list = catch_src(content)
    except ParseError:
        return content

    replace_table = []
    for src in src_list:
        src_new = save_image_src(src)
        replace_table.append((src, src_new))

    # Assume that there is no duplicated img src
    for src, src_new in replace_table:
        content = content.replace(src, src_new)

    return content


def get_file_extension(decoded_file):
    extension = imghdr.what('whatever-value', decoded_file)
    extension = "jpg" if extension == "jpeg" else extension
    return extension


# ref) http://stackoverflow.com/questions/28036404/django-rest-framework-upload-image-the-submitted-data-was-not-a-file
def save_screen_shot(data):
    # Check if the base64 string is in the "data:" format
    if 'data:' in data and ';base64,' in data:
        # Break out the header from the base64 content
        header, data = data.split(';base64,')

    # Try to decode the file. Return validation error if it fails.
    try:
        decoded_file = base64.b64decode(data)
    except TypeError:
        print('something wrong HERE')
        return

    extension = get_file_extension(decoded_file)
    path_dated, path_system = make_path(extension)

    # Write image, return media path
    with open(path_system, "wb") as f:
        f.write(decoded_file)

    path_media = MEDIA_URL[0:-1] + path_dated
    return path_media
