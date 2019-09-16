import requests

from django.shortcuts import render
from .models import Topic ,Entry
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.

'''
def index(request):
    
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')
    #将请求的数据套用到模板中，然后返回给浏览器
    #第一个参数是原始请求对象，第二个是可用于创建网页的模板
'''
def index(request):
    '''学习笔记主页'''
    return render(request,'learning_logs/index.html')
   
@login_required#加@的是装饰器也是一个函数，使它在topic之前运行，login_required()函数检查用户是否登录，仅当用户已登录时，
#Django才运行topics()函数，如果未登录的用户请求装饰器 @login_required 的保护页面，将重定向到 settings.py 中的 LOGIN_URL 指定的 URL。    
def topics(request):
    '''显示所有的主题'''
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')#升序排列
    #用户登录后，request对象将有一个user属性
    #一个上下文字典，传递给模板
    context={'topics':topics}#键是下面模板需要被替换的元素，值是需要被替换元素的内容
    return render(request,'learning_logs/topics.html',context)
        #生成一个网页 收到一个请求，指定模板    ，            内容加载进前面模板

@login_required        
def topic(request,topic_id):
    '''显示单个主题及其所有的条目'''
    #通过Topic的id获得所有条目
    topic=Topic.objects.get(id=topic_id)
    if topic.owner != request.user:#用户登录后，request对象将有一个user属性
        raise Http404
    #前面减号表示降序排列
    entries=topic.entry_set.order_by("-date_added")
    context={'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    '''添加新主题'''
    if request.method != 'POST':
        #为添加数据，创建一个新表单
        form=TopicForm()
    else:
        #POST提交的数据，对数据进行处理
        form=TopicForm(request.POST)#request.POST储存了用户提交的数据
        if form.is_valid():
        #通过is_valid()方法验证表单数据是否满足要求：用户是否填写了所有必不可少的字段（表单字段默认都是必填的），且输入的数据与字段类型是否一致
            
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            #调用save()时传递了参数commit=False，它让Django创建一个新的条目对象，
            #但并不立刻提交数据库，而是暂时存储在变量new_entry中，待为这个新条目对象添加了属性owner之后再提交数据库。
            
            # 该类将用户重定向到网页topics，函数reverse()根据指定的URL模型确定URL
            return HttpResponseRedirect(reverse("learning_logs:topics"))
            
    context={'form':form}
    return render(request,"learning_logs/new_topic.html",context)

@login_required    
def new_entry(request,topic_id):
    '''在特定主题中添加新条目'''
    topic=Topic.objects.get(id=topic_id)
    
    if request.method!='POST':
        #未提交数据，创建一个空表单
        form=EntryForm()
    else:
        #post提交的数据，对数据进行处理
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            #调用save()时传递了参数commit=False（第14行），它让Django创建一个新的条目对象，
            #但并不立刻提交数据库，而是暂时存储在变量new_entry中，待为这个新条目对象添加了属性topic之后再提交数据库。
            new_entry.topic=topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))
            #在重定向时，reverse()函数中传递了两个参数，URL模式的名称以及列表args，args包含要包含在URL中的所有参数。
            #相当于这种URL{% url 'learning_logs:topic' topic.id %}，都与urls.py中的URL模式匹配
    context={'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required        
def edit_entry(request,entry_id):
    '''编辑既有条目'''
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    if topic.owner != request.user:#用户登录后，request对象将有一个user属性
        raise Http404
    
    if request.method !="POST":#method可以取两个值，请求该方法使用的模式，是get还是post
        #初次请求，使用当前条目填充表单
        form=EntryForm(instance=entry)#通过参数instance=entry创建EntryForm实例，
            #该参数让Django创建一个表单，并使用既有条目对象中的信息填充它。
    else:
        #post提交的数据，对数据进行处理
        form=EntryForm(instance=entry,data=request.POST)#Django根据POST中的相关数据对entry进行修改。
        if form.is_valid():
            form.save()#这里未起作用
            
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))
            #在重定向时，reverse()函数中传递了两个参数，URL模式的名称以及列表args，args包含要包含在URL中的所有参数。
    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)       
        
        
