from django.urls import path
from .views import NewsList, CurrentNews, ArticlesList, CurrentArticles, news, CurrentPost, search, NewsCreate, \
    NewsEdit, NewsDelete, ArticlesCreate, ArticlesEdit, ArticlesDelete, subscriptions

urlpatterns = [
    path('news/', NewsList.as_view()),
       path('post/<int:pk>', CurrentPost.as_view()),
    path('post/subscriptions/', subscriptions, name='subscriptions'),
]
