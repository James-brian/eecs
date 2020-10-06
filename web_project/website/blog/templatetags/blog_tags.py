from django import template
from django.db.models import Count
from django.http import Http404
from random import randint

register = template.Library()
from taggit.models import Tag
from ..models import Article,Post,Comment,ArticleCategory

@register.simple_tag 
def total_articles():
	return Article.objects.count()

@register.simple_tag 
def total_posts():
	return Post.objects.count()

@register.inclusion_tag('blog/snippets/latest_articles.html')
def recent_articles(count=4):
	article_list = Article.objects.all().order_by("-date_posted")[:count]
	return {'article_list':article_list}

@register.inclusion_tag('blog/snippets/popular_articles.html')
def get_most_comment_articles():
	article_list = Article.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:7]
	return {'article_list':article_list}

@register.inclusion_tag('blog/snippets/related_articles.html')
def most_votes(count=7):
	emojis = ['🥇','🥈','🥉','🔼']
	article_list = Article.objects.all().annotate(total_comments=Count('comments')).order_by("-likes","-total_comments")[:count]
	mylist = zip(emojis,article_list)
	return {'mylist':mylist}


@register.inclusion_tag('blog/snippets/categories.html')
def cats():
	cat_list = ArticleCategory.objects.all()
	return {'cat_list':cat_list}

@register.inclusion_tag('blog/snippets/different_icons.html')
def tag_list():
    article_list = Article.objects.all().order_by("-date_posted")
    common_tags = Article.tags.most_common()[:4]
    return {'article_list':article_list,'common_tags':common_tags}


@register.inclusion_tag('blog/snippets/random_posts.html')
def random_posts():
	random_posts = Post.objects.all().order_by('?')[:5]
	return {'random_posts':random_posts}

@register.inclusion_tag('blog/snippets/recent_posts.html')
def recent_posts(count=4):
	post_list = Post.objects.all().order_by("-date_posted")[:count]
	return {'post_list':post_list}

@register.inclusion_tag('blog/snippets/top_articles.html')
def top_articles(count=4):
	article_list = Article.objects.all().order_by("-date_posted")[:count]
	return {'article_list':article_list}
