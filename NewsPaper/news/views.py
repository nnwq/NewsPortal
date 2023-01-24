from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, User, Category, SubscribedUsers
from .filters import NewsFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.dispatch import receiver
from django.http import JsonResponse
import json


def subscribe(request, id):
    user = request.user
    category = Category.object.get(id=id)
    SubscribedUsers.subscriber.add(user, category)


# Create your views here.
class PostList(ListView):
    model = Post
    ordering = 'time_created'
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


