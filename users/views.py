from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def register(request):
    """注册新用户"""
    if request.method != "POST":
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # 让用户自动登陆，再重定向到主页
            # 注册是要求输入两次密码，所以有password1和password2
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST["password1"])#验证用户函数
            login(request, authenticated_user)#只改了视图函数，这个函数没改
            return HttpResponseRedirect(reverse("learning_logs:index"))

    context = {"form": form}
    return render(request, "users/register.html", context)
