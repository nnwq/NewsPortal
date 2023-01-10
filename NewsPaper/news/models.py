from django.db import models
from django.db import forms
from django.contrib.auth.models import User
from datetime import datetime

blog_news_choice = (
        ('blog', 'Blog'),
        ('news', 'News')
)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.FloatField(default=0)

    def update_rating(self):
        return


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author_connection = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice_field = forms.ChoiceField(choices=blog_news_choice)
    time_created = models.DateTimeField(auto_now_add=True, )
    category_connection = models.ManyToManyField(Category, through='PostCategory')
    object_title = models.CharField(max_length=255)
    object_content = models.TextField()
    object_rating = models.FloatField(default=0)

    def like(self,):
        self.object_rating += 1
        self.save()

    def dislike(self,):
        self.object_rating -= 1
        self.save()

    def preview(self,):
        return()


class PostCategory(models.Model):
    post_connection = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_connection = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_connection = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_connection = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField()

    def like(self,):
        self.comment_rating += 1
        self.save()

    def dislike(self,):
        self.comment_rating -= 1
        self.save()
