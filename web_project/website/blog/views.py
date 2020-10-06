from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import Post,Article,Category,Comment,ArticleCategory,Terms,Privacy
from .statistics import Dispersion,converter,CentralTendency,Correlation
from .probability import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from .forms import ArticleForm

from taggit.models import Tag



def home(request):

    return render(request,'blog/index.html');

def about(request):

    return render(request,'blog/about.html');

def blog(request):
    posts = Post.objects.all()  
    return render(request,'blog/blog.html',{'posts': posts});

def contact(request):

    if request.method == 'POST':
        message = request.POST['message']
        name = request.POST['name']
        mail = request.POST['mail']
        country = request.POST['country']

        send_mail(name,
            mail,
            country,
            subject,
            ['brianoigo785@gmail.com'],
        fail_silently=False,)
    return render(request,'blog/contact.html');

def term(request):
    terms = Terms.objects.all()  
    return render(request,'blog/terms.html',{'terms': terms});

def privacy(request):
    pivs = Privacy.objects.all()  
    return render(request,'blog/privacy.html',{'pivs': pivs});



def singleblogbase(request):
    articles = Article.objects.all()

    return render(request, 'blog/singleblogbase.html',{'articles':articles})


class PostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    cats = Category.objects.all()
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self,*args,**kwargs):
        cat_menu = Category.objects.all()
        context = super(PostListView,self).get_context_data()
        context["cat_menu"] = cat_menu
        return context

class PostDetailView(DetailView):
    model = Post
    def get_context_data(self,*args,**kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetailView,self).get_context_data()
        context["cat_menu"] = cat_menu
        return context

class ArticleListView(ListView):
    model = Article
    template_name = 'blog/articles.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'articles'
    ordering = ['-date_posted']
    paginate_by = 7

    def get_context_data(self,*args,**kwargs):
        common_tags = Article.tags.most_common()
        cat_menu = ArticleCategory.objects.all()
        context = super(ArticleListView,self).get_context_data()
        context["cat_menu"] = cat_menu
        context["common_tags"] = common_tags
        return context


class UserArticleListView(ListView):
    model = Article
    template_name = 'blog/user_articles.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'articles'
    paginate_by = 7

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self,*args,**kwargs):
        common_tags = Article.tags.most_common()
        cat_menu = ArticleCategory.objects.all()
        context = super(UserArticleListView,self).get_context_data()
        context["cat_menu"] = cat_menu
        context["common_tags"] = common_tags
        return context

class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self,*args,**kwargs):
        #similar_articles = Article.objects.filter(tags__in=tags)
        stuff = get_object_or_404(Article, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context = super(ArticleDetailView,self).get_context_data()
        cats = ArticleCategory.objects.all()

        article = get_object_or_404(Article,id=self.kwargs['pk'])
        # List of similar books
        tags = article.tags.all()
        similar_articles = Article.objects.filter(tags__in=tags).exclude(id=article.id).distinct()

        liked = False 
        if stuff.likes.filter(id=self.request.user.id):
            liked = True 

        context["total_likes"] =  total_likes
        context["liked"] = liked 
        context["similar_articles"] = similar_articles
        #context["tags"] = tags
        return context


class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    form_class = ArticleForm


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  



class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = '/articles/'

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False


def CategoryView(request,cat):
    common_tags = Article.tags.most_common()
    cat_menu = ArticleCategory.objects.all()
    category_articles = Article.objects.filter(category=cat.replace('_',' '))
    paginate_by = 7
    ordering = ['date_posted']

    return render(request,'blog/categories.html',{'cat':cat.replace('-',' ').title(),'category_articles':category_articles,'cat_menu':cat_menu,'common_tags':common_tags})

def BlogCategoryView(request,cat):
    paginate_by = 5
    cat_menu = Category.objects.all()
    category_posts = Post.objects.filter(category=cat.replace('_',' '))
    ordering = ['date_posted']

    return render(request,'blog/blogcategories.html',{'cat':cat.replace('-',' ').title(),'category_posts':category_posts,'cat_menu':cat_menu})

def LikeView(request, pk):
    article = get_object_or_404(Article,id =request.POST.get('article_id'))
    liked = False
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('article-detail',args=[str(pk)]))


class AddCommentView(LoginRequiredMixin,CreateView):
    model = Comment
    fields = ['comment']

    def form_valid(self, form):
        form.instance.article_id = self.kwargs['pk']
        form.instance.name = self.request.user
        return super().form_valid(form)
    success_url = '/articles/'

class TagListView(ListView):
    template_name = "blog/articles.html"
    article_list = Article.objects.all().order_by("-date_posted")
    paginate_by = 7

    def get_queryset(self):
        return Article.objects.filter(tags__slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        cat_menu = ArticleCategory.objects.all()
        common_tags = Article.tags.most_common()    
        context = super(TagListView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        context["cat_menu"] = cat_menu
        context["common_tags"] = common_tags
        return context

def detail_view(request, id):
    article = get_object_or_404(Article,id=id)
    # List of similar books
    tags = article.tags.all()
    similar_articles = Article.objects.filter(tags__in=tags).exclude(id=article.id).distinct()

    return render(request,"blog/articlebase.html",{"tags": tags, "similar_articles": similar_articles})


def stats_prob(request):

    return render(request,'blog/calcindex.html');

@login_required(login_url="login")
def correlation(request):

    return render(request,'blog/correlation.html');

def dispersion(request):

    return render(request,'blog/dispersion.html');

def central_tendency(request):

    return render(request,'blog/central_tendency.html');

def normal_distribution(request):

    return render(request,'blog/normal_distribution.html');

@login_required(login_url="login")
def binomial_distribution(request):

    return render(request,'blog/binomial_distribution.html');

#*******************************central tendency**************************************************#

def covariance_correlation_answer(request):
    dataA = request.POST['query']
    dataB = request.POST['queryb']
    
    try:
        d = Correlation(converter(dataA),converter(dataB))
        cov = d.covariance(converter(dataA),converter(dataB))
        cor = d.correlation()

        my_dic = {
            'cov':cov,
            'cor':cor,
            'error':False,
            'result':True

        }
        
        return render(request,'blog/correlation.html',context=my_dic)

    except:
        my_dic = {
            'error':True,
            'result':False
        }
        
        return render(request,'blog/correlation.html',context=my_dic)

def dispersion_answer(request):
    dataA = request.POST['query']
    
    try:
        d = Dispersion(converter(dataA))
        mean = d.mean()
        var = d.variance(converter(dataA))
        stdev = d.standard_deviation(converter(dataA))
        iqr = d.interquartile_range()

        my_dic = {
            'mean':mean,
            'var':var,
            'stdev':stdev,
            'iqr':iqr,

            'error':False,
            'result':True

        }
        
        return render(request,'blog/dispersion.html',context=my_dic)

    except:
        my_dic = {
            'error':True,
            'result':False
        }
        
        return render(request,'blog/dispersion.html',context=my_dic)

def central_tendency_answer(request):
    dataA = request.POST['query']
    
    try:
        d = CentralTendency(converter(dataA))
        mean = d.mean()
        median = d.median()
        mode = d.mode()


        my_dic = {
            'dataA':dataA,
            'mean':mean,
            'median':median,
            'mode':mode,
            'error':False,
            'result':True

        }
        
        return render(request,'blog/central_tendency.html',context=my_dic)

    except:
        my_dic = {
            'error':True,
            'result':False
        }
        
        return render(request,'blog/central_tendency.html',context=my_dic)

#*******************************normal distribution**************************************************#

def normal_pdf_answer1(request):

    with verrou:
        xs = [x/10.0 for x in range(-100,100)]

        c = random.random() + 0.1
        k = round(c,1) 
        d = random.random() - 0.1
        p = round(d,1) 
        e = random.random() + 0.1 
        f = np.round(e,1)
        g = random.random() - 0.1 
        h = np.round(g,1)

        n = random.randint(-1,5)
        q = random.randint(-1,5)


        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        #plt.rc_context({
        #"figure.facecolor":  "black",  
        #"axes.facecolor":  "black",
        #"savefig.facecolor": "black",
        #"xtick.color":"white", 
        #"ytick.color":"white",
        "axes.edgecolor":"grey"
        #"axes.grid":True,
        #"grid.alpha" :1,
        #"grid.color" : "white",
        #"grid.linestyle":"--"
        })
        canvas = FigureCanvas(fig)

        plt.plot(xs,[normal_pdf(x,mu=n,sigma=k) for x in xs],'--',label='μ={0} & σ={1}'.format(n,k))
        plt.plot(xs,[normal_pdf(x,mu=n,sigma=p) for x in xs],'-.',label='μ={0} & σ={1}'.format(n,p))
        plt.plot(xs,[normal_pdf(x,mu=q,sigma=f) for x in xs],':',label='μ={0} & σ={1}'.format(q,f)) 
        plt.plot(xs,[normal_pdf(x,mu=q,sigma=h) for x in xs],'-',label='μ={0} & σ={1}'.format(q,h)) 

        plt.legend(loc='upper left')#bottom right 
        #legend = plt.legend(loc=4)
        #plt.setp(legend.get_texts(), color='w')
        plt.title("Normal  pdfs") 


        #plt.grid(True, color='white')
        plt.grid(b=True, which='major', color='grey', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()

        #plt.show()
        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png')
        return response



def normal_cdf_answer1(request):

    with verrou:

        xs = [x/10.0 for x in range(-100,100)]
        c = random.random() + 0.1
        k = round(c,1) 
        d = random.random() - 0.1
        p = round(d,1) 
        e = random.random() + 0.1 
        f = np.round(e,1)
        g = random.random() - 0.1 
        h = np.round(g,1)


        n = random.randint(-1,5)
        q = random.randint(-1,5)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        "axes.edgecolor":"grey"
        })

        canvas = FigureCanvas(fig)

        plt.plot(xs,[normal_cdf(x,mu=n,sigma=k) for x in xs],'--',label='μ={0} & σ={1}'.format(n,k))
        plt.plot(xs,[normal_cdf(x,mu=n,sigma=p) for x in xs],'-.',label='μ={0} & σ={1}'.format(n,p))
        plt.plot(xs,[normal_cdf(x,mu=q,sigma=f) for x in xs],':',label='μ={0} & σ={1}'.format(q,f)) 
        plt.plot(xs,[normal_cdf(x,mu=q,sigma=h) for x in xs],'-',label='μ={0} & σ={1}'.format(q,h))  
            
        plt.legend(loc='upper left')
        plt.title("Normal cumulative distribution functions") 


        plt.grid(b=True, which='major', color='grey', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()
        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png')
        return response
def normal_pdf_answer2(request):

    with verrou:
        xs = [x/10.0 for x in range(-100,100)]
        c = random.random() + 0.1
        k = round(c,1) 
        d = random.random() - 0.1
        p = round(d,1) 
        e = random.random() + 0.1 
        f = np.round(e,1)
        g = random.random() - 0.1 
        h = np.round(g,1)


        n = random.randint(-1,5)
        q = random.randint(-1,5)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        "axes.edgecolor":"grey"
        })

        canvas = FigureCanvas(fig)

        plt.plot(xs,[normal_pdf(x,mu=n,sigma=k) for x in xs],'--',label='μ={0} & σ={1}'.format(n,k))
        plt.plot(xs,[normal_pdf(x,mu=n,sigma=p) for x in xs],'-.',label='μ={0} & σ={1}'.format(n,p))
        plt.plot(xs,[normal_pdf(x,mu=q,sigma=f) for x in xs],':',label='μ={0} & σ={1}'.format(q,f)) 
        plt.plot(xs,[normal_pdf(x,mu=q,sigma=h) for x in xs],'-',label='μ={0} & σ={1}'.format(q,h))  
       
        plt.legend(loc='upper right')
        plt.title("Normal probability density functions") 


        plt.grid(b=True, which='major', color='grey', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()

        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png')
        return response



def normal_cdf_answer2(request):

    with verrou:

        xs = [x/10.0 for x in range(-100,100)]
        c = random.random() + 0.1
        k = round(c,1) 
        d = random.random() - 0.1
        p = round(d,1) 
        e = random.random() + 0.1 
        f = np.round(e,1)
        g = random.random() - 0.1 
        h = np.round(g,1)
 

        n = random.randint(-1,5)
        q = random.randint(-1,5)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        
        "axes.edgecolor":"grey"
       
        })

        canvas = FigureCanvas(fig)

        plt.plot(xs,[normal_cdf(x,mu=n,sigma=k) for x in xs],'--',label='μ={0} & σ={1}'.format(n,k))
        plt.plot(xs,[normal_cdf(x,mu=n,sigma=p) for x in xs],'-.',label='μ={0} & σ={1}'.format(n,p))
        plt.plot(xs,[normal_cdf(x,mu=q,sigma=f) for x in xs],':',label='μ={0} & σ={1}'.format(q,f)) 
        plt.plot(xs,[normal_cdf(x,mu=q,sigma=h) for x in xs],'-',label='μ={0} & σ={1}'.format(q,h))  
            
        plt.legend(loc=4)
        plt.title("Normal cumulative distribution functions") 


        plt.grid(b=True, which='major', color='grey', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()
        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png')
        return response


def normal_pdf_answer3(request):
    data = request.POST['querya']

    with verrou:

        try:
            xs = converter(data) 
            c = random.random() + 0.1
            k = round(c,1) 
            d = random.random() - 0.1
            p = round(d,1) 
            e = random.random() + 0.1 
            f = np.round(e,1)
            g = random.random() - 0.1 
            h = np.round(g,1)


            n = random.randint(-1,5)
            q = random.randint(-1,5)

            fig = Figure()
            plt.rcParams.update({
            "axes.edgecolor":"grey"
            })

            canvas = FigureCanvas(fig)

            plt.plot(xs,[normal_pdf(x,mu=n,sigma=k) for x in xs],'--',label='μ={0} & σ={1}'.format(n,k))
            plt.plot(xs,[normal_pdf(x,mu=n,sigma=p) for x in xs],'-.',label='μ={0} & σ={1}'.format(n,p))
            plt.plot(xs,[normal_pdf(x,mu=q,sigma=f) for x in xs],':',label='μ={0} & σ={1}'.format(q,f)) 
            plt.plot(xs,[normal_pdf(x,mu=q,sigma=h) for x in xs],'-',label='μ={0} & σ={1}'.format(q,h))  
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
            plt.title("Normal probability density functions") 


            plt.grid(b=True, which='major', color='grey', linestyle='-')
            plt.minorticks_on()
            plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
            buffer = io.BytesIO()

            plt.savefig(buffer,format='png')
            plt.close()
            response = HttpResponse(buffer.getvalue(),content_type='image/png')
            return response

        except Exception:

            my_dic = {
            'error':True
            }
        
            return render(request,'blog/normal_distribution.html',context=my_dic)


def normal_pdf_answer4(request):

    dataB = request.POST['queryb']
    dataC = request.POST['queryc']
    dataD = request.POST['queryd']
    with verrou:
        try:

            xs = converter(dataB)


            fig = Figure()
            plt.rcParams.update({
            "axes.edgecolor":"grey"
            })

            canvas = FigureCanvas(fig)

            plt.plot(xs,[normal_pdf(x,mu=float(dataC),sigma=float(dataD)) for x in xs],'-',label='μ={0} & σ={1}'.format(dataC,dataD))
            plt.title("Normal probability density curve") 


            plt.grid(b=True, which='major', color='grey', linestyle='-')
            plt.minorticks_on()
            plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
            buffer = io.BytesIO()

            plt.savefig(buffer,format='png')
            plt.close()


            response = HttpResponse(buffer.getvalue(),content_type='image/png')
            return response
        except Exception:
            my_dic = {
            'er':True
            }
        
            return render(request,'blog/normal_distribution.html',context=my_dic)





def normal_cdf_answer3(request):
    data = request.POST['querye']

    with verrou:
        try:
            xs = converter(data)

            c = random.random() + 0.1
            k = round(c,1) 
            d = random.random() - 0.1
            p = round(d,1) 
            e = random.random() + 0.1 
            f = np.round(e,1)
            g = random.random() - 0.1 
            h = np.round(g,1)

            n = random.randint(-1,5)
            q = random.randint(-1,5)            

            fig = Figure(figsize=(8, 6), dpi=80)
            plt.rcParams.update({ 
            "axes.edgecolor":"grey"
            })

            canvas = FigureCanvas(fig)

            plt.plot(xs,[normal_cdf(x,mu=n,sigma=k) for x in xs],'--',label='μ={0} & σ={1}'.format(n,k))
            plt.plot(xs,[normal_cdf(x,mu=n,sigma=p) for x in xs],'-.',label='μ={0} & σ={1}'.format(n,p))
            plt.plot(xs,[normal_cdf(x,mu=q,sigma=f) for x in xs],':',label='μ={0} & σ={1}'.format(q,f)) 
            plt.plot(xs,[normal_cdf(x,mu=q,sigma=h) for x in xs],'-',label='μ={0} & σ={1}'.format(q,h))  
            
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)          
            plt.title("Normal cumulative distribution functions") 


            plt.grid(b=True, which='major', color='grey', linestyle='-')
            plt.minorticks_on()
            plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
            buffer = io.BytesIO()
            plt.savefig(buffer,format='png')
            plt.close()


            response = HttpResponse(buffer.getvalue(),content_type='image/png')
            return response
        except Exception:
            my_dic = {
            'err':True
            }
        
            return render(request,'blog/normal_distribution.html',context=my_dic)





def normal_cdf_answer4(request):
    dataF = request.POST['queryf']
    dataG = request.POST['queryg']
    dataH = request.POST['queryh']
    with verrou:
        try:

            xs = converter(dataF)

            fig = Figure()
            plt.rcParams.update({
            "axes.edgecolor":"grey"
            })

            canvas = FigureCanvas(fig)

            plt.plot(xs,[normal_cdf(x,mu=float(dataG),sigma=float(dataH)) for x in xs],'-',label='μ={} & σ={}'.format(dataG,dataH)) 
            
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)  
            plt.title("Cdf with a mean of {0} and standard deviation of {1}".format(dataG,dataH)) 
            plt.grid(b=True, which='major', color='grey', linestyle='-')
            plt.minorticks_on()
            plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
            buffer = io.BytesIO()
            plt.savefig(buffer,format='png')
            plt.close()


            response = HttpResponse(buffer.getvalue(),content_type='image/png')
            return response
        except Exception:
            my_dic = {
            'erro':True
            }
        
            return render(request,'blog/normal_distribution.html',context=my_dic)


#*******************************binomial distribution**************************************************#
def binom_pmf_answer1(request):

    with verrou:
        c = random.uniform(0.1,0.9)
        p = round(c,2)

        n = random.randint(6,10)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        "axes.edgecolor":"grey"
        })

        canvas = FigureCanvas(fig)

        r_values = list(range(n + 1)) 
        dist = [binom.pmf(r, n, p) for r in r_values ] 
        plt.plot(r_values,dist,"o", color="blue")
        plt.title("Binomial  pmf with n = {0} and p = {1}".format(n,p)) 

        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()

        #plt.show()
        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png')
        return response



def binom_cdf_answer1(request):

    with verrou:
        c = random.uniform(0.1,0.9)
        p = round(c,2)

        n = random.randint(6,10)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        "axes.edgecolor":"grey"
        })

        canvas = FigureCanvas(fig)

        r_values = list(range(n + 1)) 
        dist = [binom.cdf(r, n, p) for r in r_values ] 
        plt.plot(r_values,dist,"o", color="blue")
        plt.title("Binomial cdf with n = {0} and p = {1}".format(n,p)) 

        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()

        #plt.show()
        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png')
        return response

def binom_pmf_answer2(request):

    with verrou:
        c = random.uniform(0.1,0.9)
        p = round(c,2)

        n = random.randint(6,10)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        "axes.edgecolor":"grey"
        })

        canvas = FigureCanvas(fig)

        r_values = list(range(n + 1))

        dist = [binom.pmf(r, n, p) for r in r_values ] 

        plt.bar(r_values, dist) 

        plt.title("Binomial  pmf with n = {0} and p = {1}".format(n,p)) 

        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()

        #plt.show()
        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png')
        return response




def binom_cdf_answer2(request):

    with verrou:

        c = random.uniform(0.1,0.9)
        p = round(c,2)

        n = random.randint(6,10)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        "axes.edgecolor":"grey"
        })

        canvas = FigureCanvas(fig)

        r_values = list(range(n + 1))
         
        dist = [binom.cdf(r, n, p) for r in r_values ] 

        plt.bar(r_values, dist) 

        plt.title("Binomial cdf with n = {0} and p = {1}".format(n,p)) 

        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()

        #plt.show()
        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png')
        return response



def binom_pmf_answer3(request):
    data = request.POST['querya']
    datax = request.POST['queryx']

    with verrou:

        p = float(data)

        n = int(datax)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        "axes.edgecolor":"grey"
        })

        canvas = FigureCanvas(fig)

        r_values = list(range(n + 1))

        dist = [binom.pmf(r, n, p) for r in r_values ] 

        plt.plot(r_values,dist,"o", color="blue")

        plt.title("Binomial pmf with n = {0} and p = {1}".format(n,p)) 

        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()

        #plt.show()
        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png')
        return response


def binom_pmf_answer4(request):

    dataB = request.POST['queryb']
    dataC = request.POST['queryc']
    with verrou:
        
        p = float(dataB)

        n = int(dataC)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        "axes.edgecolor":"grey"
        })

        canvas = FigureCanvas(fig)

        r_values = list(range(float(n) + 1))

        dist = [binom.pmf(r, n, p) for r in r_values ] 

        plt.bar(r_values, dist) 

        plt.title("Binomial pmf with n = {0} and p = {1}".format(n,p)) 

        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()

        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png') 
        return response



def binom_cdf_answer3(request):
    data = request.POST['querye']
    dataN = request.POST['queryn']

    with verrou:
    
        p = float(data)

        n = int(dataN)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        "axes.edgecolor":"grey"
        })

        canvas = FigureCanvas(fig)

        r_values = list(range(n + 1))

        dist = [binom.cdf(r, n, p) for r in r_values ] 

        plt.plot(r_values,dist,"o", color="blue")

        plt.title("Binomial cdf with n = {0} and p = {1}".format(n,p)) 

        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()

        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png')
        return response

       


def binom_cdf_answer4(request):
    dataF = request.POST['queryf']
    dataG = request.POST['queryg']
    with verrou:
        p = float(dataF)

        n = int(dataG)

        fig = Figure(figsize=(8, 6), dpi=80)
        plt.rcParams.update({
        "axes.edgecolor":"grey"
        })

        canvas = FigureCanvas(fig)

        r_values = list(range(n + 1))

        dist = [binom.cdf(r, n, p) for r in r_values ] 

        plt.bar(r_values, dist) 

        plt.title("Binomial cdf with n = {0} and p = {1}".format(n,p)) 

        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='white', linestyle='-', alpha=0.2)
        buffer = io.BytesIO()

        plt.savefig(buffer,format='png')
        plt.close()


        response = HttpResponse(buffer.getvalue(),content_type='image/png') 
        return response

    