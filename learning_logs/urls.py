from django.urls import path
#从当前的urls.py模块所在的文件夹中导入视图
from . import views

#添加命名空间
app_name='learning_logs'
#改变量包含该app中可请求的网页
urlpatterns=[
    #主页
    path('',views.index,name='index'),
    path("topics/",views.topics,name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    #             正则表达式捕获topic_id,并将这个整数存储在一个名为 topic_id实参中
    #用于添加新主题的网站
    path("new_topic/",views.new_topic,name='new_topic'),#当用户要添加新主题时，将切换到http://localhost:8000/new_topic/ 。
    path("new_entry/<int:topic_id>/",views.new_entry,name='new_entry'),
    #编辑已有的条目网站
    path("edit_entry/<int:entry_id>/",views.edit_entry,name='edit_entry'),
    #匹配词（word）的开始（\<）和结束（\>）。例如正则表达式\<the\>能够匹配字符串"for the wise"中的"the"，
    #path()的第一个参数是正则表达式，第二个参数是要调用的视图函数（当请求的URL和第一个参数匹配时调用），
    #第三个参数为这个URL模式指定一个名字，相当于将这个模式保存在变量index中，以后每当需要提供这个主
    #页的连接时都使用这个名字，而不用再编写URL。
]
