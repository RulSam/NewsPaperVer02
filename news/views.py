from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Category, Post
from .filters import PostFilter
from .forms import (CategoryForm, NewsForm, ArticlesForm)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class CategoryList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Category
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'nm_category'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'category.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'category'

class CategoryDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Category
    # Используем другой шаблон — product.html
    template_name = 'categoryOne.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'categoryOne'

class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'post_title'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    context_object_name = 'news'  # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    ordering = ['-date_time_create']  #Новости должны выводиться в порядке от более свежей к старой.

    paginate_by = 2  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostSearch(PostList):
    template_name = 'newsSearch.html'

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'newsOne.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'newsOne'

def create_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/category/')

    return render(request, 'categoryEdit.html', {'form': form})

# def create_news(request):
#     form = NewsForm()
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#
#     return render(request, 'postEdit.html', {'form': form})

class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'postEdit.html'

class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'postEdit.html'

class NewsDelete(DeleteView):
    model = Post
    template_name = 'postDelete.html'
    success_url = reverse_lazy('news')

class ArticlesCreate(CreateView):
    form_class = ArticlesForm
    model = Post
    template_name = 'articlesEdit.html'

class ArticlesUpdate(UpdateView):
    form_class = ArticlesForm
    model = Post
    template_name = 'articlesEdit.html'

class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'articlesDelete.html'
    success_url = reverse_lazy('news')