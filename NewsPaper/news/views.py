from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, User
from .filters import NewsFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.db.models.signals import post_save
from django.dispatch import receiver


def send_email_to_subscribers(sender, instance, created, **kwargs):
    subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )


post_save.connect(send_email_to_subscribers(), sender=Post)


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
    msg = EmailMultiAlternatives(
        subject=f'{Post.object_title}',
        body='Hello, 'f'{User.username}''! New post is in your favourite category!',
        from_email='',
        to=[''],
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


