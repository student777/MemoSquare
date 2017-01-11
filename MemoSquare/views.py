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


from rest_framework.decorators import api_view
@api_view(['PUT'])
def upload(request, filename):
    from .serializers import ImageSerializer
    serializer = ImageSerializer(data=request.data)
    serializer.to_internal_value(request.data)
    serializer.is_valid()
    print(serializer.data['image'])
    return Response('dddd')