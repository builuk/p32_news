from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),

    path('bookmarks/', views.BookmarkListView.as_view(), name='bookmark_list'),
    path('articles/<slug:slug>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('weather/', views.weather_view, name='weather'),
]