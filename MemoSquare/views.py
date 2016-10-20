from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def sign_in(request):
    # (Receive token by HTTPS POST)
    token = request.POST.get('idToken')
    user = authenticate(token=token)

    if user is not None:
        login(request, user)

    return HttpResponse('hello SunYoung mom, I am MoonOld father')


def sign_out(request):
    return HttpResponse('sign_out hello world')
