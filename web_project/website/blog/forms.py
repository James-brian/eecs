from django import forms
from .models import Article,ArticleCategory
from tinymce.widgets import TinyMCE


choices = ArticleCategory.objects.all().values_list('name','name')
choice_list = []
for item in choices:
	choice_list.append(item)

class ArticleForm(forms.ModelForm):
	content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
	
	class Meta:
		model = Article		 
		fields = ('title', 'content','coverimage','category','tags')

		widgets = {
		'category': forms.Select(choices=choices,attrs={'class': 'form-control'})
		}
