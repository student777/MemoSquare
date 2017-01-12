from xml.etree import ElementTree
import urllib.request
from django.utils import timezone
from MemoSquare.settings import MEDIA_ROOT, MEDIA_URL, DOMAIN
from xml.etree.ElementTree import ParseError
from PIL import Image
import os
import uuid
import imghdr
import re
import io
import base64


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

    path_dated = timezone.now().strftime('/%y/%m/%d/') + complete_file_name  # ex)/17/01/01/no_name.jpg
    path_system = MEDIA_ROOT + path_dated  # ex)/usr/local/server/MemoSquare/media/17/01/01/no_name.jpg
    path_media = DOMAIN + MEDIA_URL[0:-1] + path_dated  # ex)/media/17/01/01/no_name.jpg

    # Make directory
    os.makedirs(os.path.dirname(os.path.normpath(path_system)), exist_ok=True)

    return path_system, path_media


# Not create Memo_image foreign key, just stack images
def save_image_src(src):
    extension = os.path.splitext(src)[-1].lower()[1:]
    path_system, path_media = make_path(extension)
    # Need to async..?
    urllib.request.urlretrieve(src, path_system)
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
    return extension


# ref) http://stackoverflow.com/questions/28036404/django-rest-framework-upload-image-the-submitted-data-was-not-a-file
# I'd prefer this to Base64ImageField because of save_image_src code reusability
def save_screen_shot(data, rectangle):
    image_data = re.sub('^data:image/.+;base64,', '', data)
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))

    extension = image.format.lower()
    path_system, path_media = make_path(extension)

    # Crop and Save image
    image = image.crop(rectangle)
    image.save(path_system)

    return path_media
