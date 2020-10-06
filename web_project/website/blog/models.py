from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

#from ckeditor.fields import RichTextField
#from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from PIL import Image


# Create your models here.	
class Post(models.Model):

	title = models.CharField(max_length=50)
	content = CKEditor5Field('Your Article', config_name='extends')
	#content = RichTextUploadingField(blank=True,null=True)
	excerpt = models.CharField(max_length = 200)
	img = models.ImageField(upload_to='pics')
	category = models.CharField(max_length=50)
	date_posted = models.DateTimeField(default=timezone.now)

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})


class Article(models.Model):

	title = models.CharField(max_length=50)
	#content = CKEditor5Field('Your Article', config_name='extends')
	#content = RichTextUploadingField('Text',config_name='extends',blank=True,null=True)
	content = models.TextField()
	coverimage = models.ImageField(upload_to='coverpics')
	category = models.CharField(max_length=50)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name='blog_posts')
	tags = TaggableManager('key words')

	def __str__(self):
	    return self.title

	def get_absolute_url(self):
		return reverse('article-detail', kwargs={'pk': self.pk})

	def total_likes(self):
		return self.likes.count()

	@property
	def get_photo_url(self):
	    if self.coverimage and hasattr(self.coverimage, 'url'):
	        return self.coverimage.url
	    else:
	        return "/static/blog/Background/design.png"

	def save(self, *args, **kwargs):
	        super(Article, self).save(*args, **kwargs)

	        img = Image.open(self.coverimage.path)

	        if img.height > 300 or img.width > 300:
	            output_size = (300, 300)
	            img.thumbnail(output_size)
	            img.save(self.coverimage.path)


class Category(models.Model):

	name = models.CharField(max_length=50)

	def __str__(self):
	    return self.name

	def get_absolute_url(self):
		return reverse('blog-blog')


class Comment(models.Model):
	article = models.ForeignKey(Article, related_name="comments",on_delete=models.CASCADE)
	name = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField()
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return '%s - %s' % (self.article.title,self.name)

class ArticleCategory(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
	    return self.name

	def get_absolute_url(self):
		return reverse('blog-articles')


class Terms(models.Model):
	content = CKEditor5Field('Text', config_name='extends')
	#content = RichTextUploadingField(blank=True,null=True)
	date_posted = models.DateTimeField(default=timezone.now)

class Privacy(models.Model):
	content = CKEditor5Field('Text', config_name='extends')
	#content = RichTextUploadingField(blank=True,null=True)
	date_posted = models.DateTimeField(default=timezone.now)


