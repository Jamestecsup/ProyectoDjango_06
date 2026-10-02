from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='detail'),
    path('category/<slug:slug>/', views.article_by_category, name='by_category'),
]
