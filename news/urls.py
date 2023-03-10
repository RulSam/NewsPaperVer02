from django.urls import path
from .views import NewsList, CurrentNews, ArticlesList, CurrentArticles, news, CurrentPost, search, NewsCreate, \
    NewsEdit, NewsDelete, ArticlesCreate, ArticlesEdit, ArticlesDelete, subscriptions, IndexView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('news/', NewsList.as_view()),
    path('news/<int:pk>', CurrentNews.as_view()),
    path('articles/', ArticlesList.as_view()),
    path('articles/<int:pk>', CurrentArticles.as_view()),
    path('post/', news.as_view()),
    path('post/<int:pk>', CurrentPost.as_view()),
    path('search/', search.as_view()),
    path('news/create/', NewsCreate.as_view()),
    path('news/<int:pk>/edit/', NewsEdit.as_view()),
    path('news/<int:pk>/delete/', NewsDelete.as_view()),
    path('articles/create/', ArticlesCreate.as_view()),
    path('articles/<int:pk>/edit/', ArticlesEdit.as_view()),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view()),
    path('post/subscriptions/', subscriptions, name='subscriptions'),
    path('', IndexView.as_view()),
]