from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
import json

# Create your views here.
def login(request):
    """用户登录"""
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pwd')
        user = auth.authenticate(username=username,password=password)
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request,'login.html',{'error_msg': '用户名或密码错误!'})
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    # request.session.clear()
    return redirect('login')

def index(request):
    """主页"""
    return render(request,'index.html')