from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Report
from .magic import save_screen_shot


def index(request):
    return render(request, 'base.html')


# Facebook & Google oauth2 token login by DRF SessionAuthentication
def sign_in(request):
    if request.method == 'POST':
        token_social = request.POST.get('token')
        user = authenticate(token=token_social)
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        return HttpResponse(status=401)


# login by DRF TokenAuthentication
def sign_in_token(request):
    from rest_framework.authtoken.models import Token
    if request.method == 'POST':
        token_social = request.POST.get('token')
        user = authenticate(token=token_social)
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            return HttpResponse(token[0], status=200)
        return HttpResponse(status=401)


def sign_out(request):
    logout(request)
    return redirect('/')


@login_required
def report(request):
    if request.method == 'POST':
        user = request.user
        content = request.POST['content']
        Report.objects.create(user=user, content=content)
        return HttpResponse(status=200)


def upload(request):
    try:
        data = request.POST['image']
        rectangle = [int(i) for i in [request.POST['left'], request.POST['upper'], request.POST['right'], request.POST['lower']]]
    except KeyError:
        return HttpResponse('fuck you', status=400)
    media_path = save_screen_shot(data, rectangle)
    return HttpResponse(media_path)
