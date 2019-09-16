from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:  #它告诉Django根据哪个模型创建表单，以及在表单中包含哪些字段。
        model=Topic
        fields=['text'] #该表单只包含字段text，
        labels={'text':'标题'}  #并不为该字段生成标签
        
#创建一个与模型Entry相关联的表单
class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['text']
        labels={'text':''}
        widgets={'text': forms.Textarea(attrs={'cols':80})}
        
        
        
        
        
