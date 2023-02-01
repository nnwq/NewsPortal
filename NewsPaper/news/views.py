from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from isort.profiles import django

from .models import Post, Category, SubscribedUsers
from .filters import NewsFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.template.loader import render_to_string


class Subscribe(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'subscribe.html'
    context_object_name = 'subscribe'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        usercategory = SubscribedUsers(
            subscriber=self.request.subscriber,
            category=self.get_object()
        )
        usercategory.save()
        return redirect(f'/news/category/{self.get_object().id}/success')


# Create your views here.
class PostList(ListView):
    model = Post
    ordering = 'creation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    html_content = render_to_string(
        'post_edit.html',
    )


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class Success(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'success.html'
    context_object_name = 'success'


class Categories(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
