from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import Report


def index(request):
    return render(request, 'base.html')


# Facebook oauth2 token login
@csrf_exempt
def sign_in(request):
    token = request.POST.get('token')
    user = authenticate(token=token)
    if user is not None:
        login(request, user)
    return HttpResponse('hello %s' % user)


def sign_out(request):
    logout(request)
    return redirect('/')


# TEST? For cross browsing request(chrome extension)
def csrf_test(request):
    if request.is_ajax():
        return render(request, 'csrf_token')


@login_required
def report(request):
    if request.POST:
        user = request.user
        content = request.POST['content']
        Report.objects.create(user=user, content=content)
        return render(request, 'report_close.html')

    return render(request, 'report.html')
