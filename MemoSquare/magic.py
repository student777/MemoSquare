import urllib.request
from django.contrib.sites.models import Site
from django.utils import timezone
from MemoSquare.settings import MEDIA_ROOT, MEDIA_URL
from PIL import Image
import os
import uuid
import re
import io
import base64
from html.parser import HTMLParser


def make_path(file_extension):
    # Generate file name, extension, Get date
    file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
    complete_file_name = "%s.%s" % (file_name, file_extension)
    path_dated = timezone.now().strftime('/%y/%m/%d/') + complete_file_name  # ex)/17/01/01/no_name.jpg
    path_system = MEDIA_ROOT + path_dated  # ex)/usr/local/server/MemoSquare/media/17/01/01/no_name.jpg
    path_media = Site.objects.get_current().domain + MEDIA_URL[0:-1] + path_dated  # ex)http://memo-square.com/media/17/01/01/no_name.jpg

    # Make directory
    os.makedirs(os.path.dirname(os.path.normpath(path_system)), exist_ok=True)

    return path_system, path_media


# Not create Memo_image foreign key, just stack images
def download_image_from_src(src):
    extension = os.path.splitext(src)[-1].lower()[1:]
    path_system, path_media = make_path(extension)
    # Need to async..?
    urllib.request.urlretrieve(src, path_system)
    return path_media


class MyParse(HTMLParser):
    content_set = set()

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.content_set.add(dict(attrs)["src"])


def get_src_set(content):
    parser = MyParse()
    parser.feed(content)
    return parser.content_set


def grab_img_from_content(content):
    src_set = get_src_set(content)

    replace_table = []
    for src in src_set:
        src_new = download_image_from_src(src)
        replace_table.append((src, src_new))

    for src, src_new in replace_table:
        content = content.replace(src, src_new)

    return content


# ref) http://stackoverflow.com/questions/28036404/django-rest-framework-upload-image-the-submitted-data-was-not-a-file
# ref) http://stackoverflow.com/questions/4083702/posting-a-file-and-data-to-restful-webservice-as-json
# I'd prefer this to Base64ImageField because of download_image_from_src code reusability
def save_screen_shot(data, rectangle):
    image_data = re.sub('^data:image/.+;base64,', '', data)
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))

    extension = image.format.lower()
    path_system, path_media = make_path(extension)

    # Crop and Save image
    image = image.crop(rectangle)
    image.save(path_system)

    return path_media

