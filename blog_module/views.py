from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DeleteView, DetailView

from .models import Articles, Category, Tag, comments, Likes


# Create your views here.
def index(request):
    site_articles = Articles.objects.all()
    site_articles_last = Articles.objects.order_by('-pub_date')
    context = {
        'request': request,
        'articles' : site_articles,
        'last_articles' : site_articles_last[:3],
    }
    return render(request, 'blog_module/index.html',context)

def sidebar_partial(request):
    tags = Tag.objects.all()[:8]
    categories = Category.objects.all()[:3]
    recent_articles= Articles.objects.order_by('-pub_date')[:3]
    return render(request,'includes/sidebar.html',{'tags': tags, 'categories' : categories, 'recent_articles' :recent_articles} )


def details(request, pk):
    articles = get_object_or_404(Articles, pk=pk)
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        message = request.POST.get('message')
        comments.objects.create(article=articles, comment=message, parent_id=parent_id, author=request.user)
    return render(request, 'blog_module/post-details.html', {'articles': articles})

def articles_list(request):
    articles_list = Articles.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(articles_list, 1)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    page_number = articles.number
    page_range = range(max(page_number - 1, 1), min(page_number + 1, articles.paginator.num_pages) + 1)

    return render(request, 'blog_module/blog-list.html', {"articles": articles, "page_range": page_range})


def Tags_list(request, pk):
    Tags = get_object_or_404(Tag, id=pk)
    articles = Tags.articles_related.all()
    return render(request, 'blog_module/blog-list.html', {"articles": articles})


def search_results(request):
    query = request.GET.get('q')
    articles = Articles.objects.filter(title__icontains=query)

    paginator = Paginator(articles, 1)
    page_number = request.GET.get('page')
    object_list = paginator.get_page(page_number)

    page_range = range(max(object_list.number - 1, 1), min(object_list.number + 1, paginator.num_pages) + 1)
    return render(request, "blog_module/blog-list.html", {"articles": object_list, "page_range": page_range})


def Like(request, pk):
    try:
        like = Likes.objects.get(article_id=pk, user_id=request.user.id)
        like.delete()
    except:
        Likes.objects.create(article_id=pk, user_id=request.user.id)
    return redirect("blog_module:index")