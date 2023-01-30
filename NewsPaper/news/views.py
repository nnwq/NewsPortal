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
import django.db.models
import json


def subscribe(request, id):
    user = request.user
    category = Category.objects.get(id=id)
    Category.subscribers.add(user, category)


class NewsListFiltered(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-creation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news_flist'
    paginate_by = 10

    @staticmethod
    def is_subscribed(cat, query: django.db.models.query.QuerySet):
        for i in range(len(query)):
            if cat == str(query[i]['category_id']):
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_count'] = self.filterset.qs.count()
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['sub_button'] = False
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user
            if 'category' in self.filterset.data.keys():
                context['subscribed'] = self.is_subscribed(self.filterset.data['category'],
                                                           SubscribedUsers.objects.filter(user_id=self.request.user).values('category_id'))
                if self.filterset.data['category'] != '':
                    context['sub_button'] = True

        return context

   # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        queryset = Post.objects.order_by('-creation')
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs


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


