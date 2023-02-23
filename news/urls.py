from django.urls import path
from .views import news, CurrentPost,  

urlpatterns = [
    path('news/', NewsList.as_view()),
       path('post/<int:pk>', CurrentPost.as_view()),
    
]
