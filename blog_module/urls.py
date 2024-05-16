from django.urls import path
from . import views

app_name = 'blog_module'
urlpatterns = [
    path('', views.index, name='index'),
    path('sidebar', views.sidebar_partial, name='sidebar_partial'),

    path('<int:pk>/', views.details, name='details'),
    path('blog/', views.articles_list, name='blog_list'),
    path('tag/<pk>', views.Tags_list, name='Tags_list'),
    path('search/', views.search_results, name='search'),
    path('like/<int:pk>', views.Like, name='like'),
]