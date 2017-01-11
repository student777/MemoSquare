from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework import views, status
from rest_framework.parsers import FileUploadParser, MultiPartParser
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


# views.py
class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)
    # parser_classes = (MultiPartParser,)

    def put(self, request, filename, format=None):
        print(request.body)
        f = request.data['file']
        # print(request.FILES['file'])
        # with open('/home/yee/Downloads/Failed.py', 'w') as f:
        #     f.write('whatever')
        with open('/home/yee/Downloads/'+filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return Response(status=status.HTTP_204_NO_CONTENT)
