from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from .models import Report


def index(request):
    return render(request, 'base.html')


# Facebook & Google oauth2 token login
@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        user = authenticate(token=token)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


def sign_out(request):
    logout(request)
    return redirect('/')


# TEST? For cross browsing request(chrome extension)
def csrf_test(request):
    if request.is_ajax():
        return render(request, 'csrf_token')


@login_required
def report(request):
    if request.method == 'POST':
        user = request.user
        content = request.POST['content']
        Report.objects.create(user=user, content=content)
        return render(request, 'report_close.html')

    return render(request, 'report.html')


def upload(request):
    # imagestr = request.POST['image']
    # imagestr = str.encodde(imagestr)
    # from base64 import decodebytes
    #
    # with open("/home/yee/Downloads/foo.png", "wb") as f:
    #     f.write(decodebytes(imagestr))
    #
    # from django.http import HttpResponse
    # return HttpResponse('new src')

    #ref) http://stackoverflow.com/questions/28036404/django-rest-framework-upload-image-the-submitted-data-was-not-a-file
    import base64
    import uuid
    import os
    from MemoSquare.settings import MEDIA_ROOT, MEDIA_URL
    from django.utils import timezone
    data = request.POST['image']
    # Check if the base64 string is in the "data:" format
    if 'data:' in data and ';base64,' in data:
        # Break out the header from the base64 content
        header, data = data.split(';base64,')
    extension = header[11:]
    random_name = uuid.uuid4().hex
    img_path = timezone.now().strftime('/%y/%m/%d/') + random_name + '.' + extension
    path_to_save = MEDIA_ROOT + img_path
    # Try to decode the file. Return validation error if it fails.
    try:
        decoded_file = base64.b64decode(data)
    except TypeError:
        pass

    os.makedirs(os.path.dirname(os.path.normpath(path_to_save)), exist_ok=True)

    with open(path_to_save, "wb") as f:
        f.write(decoded_file)
    src_new = MEDIA_URL[0:-1] + img_path
    from django.http import HttpResponse
    return HttpResponse(src_new)
