from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Topic(models.Model):
    '''用户学习的主题'''
    text=models.CharField(max_length=200)#标题文本
    date_added=models.DateTimeField(auto_now_add=True)#auto_now=Ture，字段保存时会自动保存当前时间
    #auto_now_add=True，字段在实例第一次保存的时候会保存当前时间
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    #添加一个关联到用户的外键
    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text

class Entry(models.Model):#是在topic下添加的条目模型，与topic是一对多的关系
    '''学到有关某个主题的具体知识'''
    #由于和主题是一对多的关系，所以主题是条目的外键
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    text=models.TextField()#正文文本
    date_added=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural='entries'
        #verbose_name指定在admin管理界面中显示中文；verbose_name表示单数形式的显示，verbose_name_plural表示复数形式的显示
        
    def __str__(self):
        '''返回模型的字符串表示'''
        #由于条目可能很长只显示前50个字符
        if len(self.text)>50:
            return self.text[:50]+'...'
        else:
            return self.text
