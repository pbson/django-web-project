from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password_repeat = request.POST['password-repeat']
        email = request.POST['email']
        username = request.POST['username']

        if password == password_repeat:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username,email,password,first_name=first_name,last_name=last_name)
                user.save()
                print('user created')
                messages.warning(request, "Successfully registerd")
                return redirect('/')
        else:
            messages.info(request,'Password not matching')
            return redirect('register')
    else:
        return render(request,'register.html',{})

def login (request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            if 'next' in request.POST:
                messages.warning(request, "Successfully login")
                return redirect(request.POST.get('next'))   
            else:
                messages.warning(request, "Successfully registerd")
                return redirect('/')
        else:
            messages.info(request,'Invalid')
            return redirect('login')
    else:
        return render(request,'Signin.html',{})

def logout(request):
    auth.logout(request)
    if 'next' in request.POST:
        return redirect(request.POST.get('next'))
    else:
        return redirect('/')


