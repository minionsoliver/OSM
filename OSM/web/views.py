from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
def login(request):
    """用户登录"""
    return render(request,'login.html')

def logout(request):
    return

def index(request):
    """主页"""
    return render(request,'base.html')