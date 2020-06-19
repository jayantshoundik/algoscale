from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import SignUpForm
from django.contrib.auth import login as auth_login, authenticate,logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
   
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return redirect('register')
    return render(request,'adminpanel/login.html')

    

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'adminpanel/register.html', {'form': form})
    
@login_required(login_url='login')
def dashboard(request):
    users= User.objects.all()
    if request.method == 'POST':
        deleteuser= User.objects.get(id= request.POST.get('adminuserid'))
        deleteuser.delete()
    return render(request,'adminpanel/dashboard.html',{'users': users})
def logout(request):
    auth_logout(request)
    return redirect('login')