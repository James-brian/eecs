from django.contrib import admin
from .models import Post,Article,Category,Comment,ArticleCategory,Terms,Privacy
# Register your models here.
#class ArticleAdmin(admin.ModelAdmin):
#	class Media:
#		css = {
#		"all": ("css/tinymce.css",)
#		}

#		js = ("js/blog.js",)

#admin.site.register(Article, ArticleAdmin)

admin.site.register(Post)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ArticleCategory)
admin.site.register(Terms)
admin.site.register(Privacy)

