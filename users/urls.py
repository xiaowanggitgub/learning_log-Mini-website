from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path
#从当前的urls.py模块所在的文件夹中导入视图
from . import views

#添加命名空间,必须设置命名空间
app_name='users'

urlpatterns=[
    #登录页面
    #这里与教程上不同，login变为了LoginView，且调用as_view方法
    path('login/',LoginView.as_view(template_name='users/login.html'),name='login'),
    #Django自带的login视图函数,这个函数中自带user变量，每个模板都可以用
    #我们渲染模板的代码都是在自己写的视图函数中。但这里使用了自带的视图函数，无需自行编写进行渲染的代码。
    #所以，我们还传了一个参数，告诉Django到哪里查找我们要用到的模板。注意，该模板在users中，而不是在learning_logs中。
    path('logout/',LogoutView.as_view(template_name='learning_logs/index.html'),name="logout"),
    path('register/',views.register,name='register'),
]
