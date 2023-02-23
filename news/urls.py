from django.urls import path
from .views import news, CurrentPost,  \
     subscriptions

urlpatterns = [
    path('news/', NewsList.as_view()),
       path('post/<int:pk>', CurrentPost.as_view()),
    path('post/subscriptions/', subscriptions, name='subscriptions'),
]
