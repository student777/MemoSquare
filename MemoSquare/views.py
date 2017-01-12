from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Report
from .magic import save_screen_shot


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
            return HttpResponse(status=200)
        return HttpResponse(status=401)


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
    try:
        data = request.POST['image']
        rectangle = [int(i) for i in [request.POST['left'], request.POST['upper'], request.POST['right'], request.POST['lower']]]
    except KeyError:
        return HttpResponse('fuck you', status=400)
    media_path = save_screen_shot(data, rectangle)
    return HttpResponse(media_path)
