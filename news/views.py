from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.cache import cache

from .forms import PostForm
from .models import Post, Category, Subscriber
from .filters import PostFilter
from .tasks import hello

from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail
from datetime import datetime

from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        return redirect('appointments:make_appointment')


class NewsList(ListView):
    model = Post
    template_name = 'NewsList.html'
    context_object_name = 'NewsList'
    def get_queryset(self):
        return Post.objects.filter(categoryType='NW').order_by('dateCreation')

class CurrentNews(DetailView):
    model = Post
    template_name = 'CurrentNews.html'
    context_object_name = 'CurrentNews'

class ArticlesList(ListView):
    model = Post
    template_name = 'ArticlesList.html'
    context_object_name = 'ArticlesList'
    def get_queryset(self):
        return Post.objects.filter(categoryType='AR').order_by('dateCreation')

class CurrentArticles(DetailView):
    model = Post
    template_name = 'CurrentArticles.html'
    context_object_name = 'CurrentArticles'

class news(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    def get_queryset(self):
        return Post.objects.filter().all().order_by('id')

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

class CurrentPost(DetailView):
    model = Post
    template_name = 'CurrentPost.html'
    context_object_name = 'CurrentPost'
    def get_queryset(self):
        return Post.objects.filter().all()

class search(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'NewsCreate.html'
    success_url = '/news/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)

class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'NewsEdit.html'
    success_url = '/news/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)

class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'NewsDelete.html'
    success_url = '/news/'

class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('articles.add_post')
    form_class = PostForm
    model = Post
    template_name = 'ArticlesCreate.html'
    success_url = '/articles/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)

class ArticlesEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('articles.change_post')
    form_class = PostForm
    model = Post
    template_name = 'ArticlesEdit.html'
    success_url = '/articles/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)

class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('articles.delete_post')
    model = Post
    template_name = 'ArticlesDelete.html'
    success_url = '/articles/'


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')

    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

class IndexView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')