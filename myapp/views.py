from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from myapp.models import Users
from .forms import UsersForm
import json
from django.db.models import Q
import datetime

def login_required_decorator(f):
    return login_required(f, login_url="main:login")

@login_required_decorator
def dashboard(request):
    return render(request, 'dashboard/index.html')

def dashboard_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:dashboard')
    return render(request, 'dashboard/login.html')

@login_required_decorator
def dashboard_logout(request):
    logout(request)
    return redirect('main:login')


@login_required_decorator
def category_list(request):
    categories = Users.objects.all()
    ctx = {"costumers": categories, "follow_active": "menu-open"}
    return render(request,'dashboard/categories/list.html',ctx)

@login_required_decorator
def category_create(request):
    model = Users()
    form = UsersForm(request.POST,request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('main:category_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/categories/form.html', ctx)

@login_required_decorator
def category_edit(request, pk):
    model = Users.objects.get(id=pk)
    form = UsersForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('main:category_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/categories/form.html', ctx)

@login_required_decorator
def category_delete(request, pk):
    model = Users.objects.get(id=pk)
    model.delete()
    return redirect('main:category_list')


@login_required_decorator
def statistic(request):
    return render(request, "dashboard/statistic.html")