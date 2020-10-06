from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    UserArticleListView,
    CategoryView,
    BlogCategoryView,
    LikeView,
    AddCommentView,
    detail_view,
    TagListView,
    ) 
from . import views


urlpatterns = [
    path('', views.home, name='blog-index'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('terms-and-conditions/', views.term, name='blog-terms'),
    path('privacy-policy/', views.privacy, name='blog-privacy'),

    path('stats_prob', views.stats_prob, name='stats-prob'),
    path('correlation', views.correlation, name='correlation'),
    path('covariance_correlation_answer',views.covariance_correlation_answer,name='covariance_correlation_answer'),
    path('dispersion_answer',views.dispersion_answer,name='dispersion_answer'),
    path('dispersion',views.dispersion,name='dispersion'),
    path('central_tendency_answer',views.central_tendency_answer,name='central_tendency_answer'),
    path('central_tendency',views.central_tendency,name='central_tendency'),

    path('normal_pdf_answer1/',views.normal_pdf_answer1,name='normal_pdf_answer1'),
    path('normal_cdf_answer1/',views.normal_cdf_answer1,name='normal_cdf_answer1'),
    path('normal_pdf_answer2/',views.normal_pdf_answer2,name='normal_pdf_answer2'),
    path('normal_cdf_answer2/',views.normal_cdf_answer2,name='normal_cdf_answer2'),
    path('normal_pdf_answer3/',views.normal_pdf_answer3,name='normal_pdf_answer3'),
    path('normal_cdf_answer3/',views.normal_cdf_answer3,name='normal_cdf_answer3'),
    path('normal_pdf_answer4/',views.normal_pdf_answer4,name='normal_pdf_answer4'),
    path('normal_cdf_answer4/',views.normal_cdf_answer4,name='normal_cdf_answer4'),

    path('binom_pmf_answer1/',views.binom_pmf_answer1,name='binom_pmf_answer1'),
    path('binom_cdf_answer1/',views.binom_cdf_answer1,name='binom_cdf_answer1'),
    path('binom_pmf_answer2/',views.binom_pmf_answer2,name='binom_pmf_answer2'),
    path('binom_cdf_answer2/',views.binom_cdf_answer2,name='binom_cdf_answer2'),
    path('binom_pmf_answer3/',views.binom_pmf_answer3,name='binom_pmf_answer3'),
    path('binom_cdf_answer3/',views.binom_cdf_answer3,name='binom_cdf_answer3'),
    path('binom_pmf_answer4/',views.binom_pmf_answer4,name='binom_pmf_answer4'),
    path('binom_cdf_answer4/',views.binom_cdf_answer4,name='binom_cdf_answer4'),

    path('normal_distribution',views.normal_distribution,name='normal_distribution'),
    path('binomial_distribution',views.binomial_distribution,name='binomial_distribution'),


    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('blog/',PostListView.as_view(),name='blog-blog'),
    path('article/<int:pk>/',ArticleDetailView.as_view(),name='article-detail'),
    path('article/new/', ArticleCreateView.as_view(), name='article-create'),

    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('user/<str:username>', UserArticleListView.as_view(), name='user-articles'),

    path('category/<str:cat>', CategoryView,name='category'),
    path('blogcategory/<str:cat>', BlogCategoryView,name='blogcategory'),
    path('like/<int:pk>', LikeView, name='like_article'),
    path('article/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
	#path('blog/', views.blog, name='blog-blog'),
 	#path('singleblog/', views.singleblog, name='blog-singleblog'),
	path('articles/', ArticleListView.as_view(),name='blog-articles'),

    path('detail/<int:id>/',detail_view,name='detail'),
    path('tagged/<slug:slug>/', TagListView.as_view(), name="tagged_articles"),
]