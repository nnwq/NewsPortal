from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

blog_news_choice = (
        ('blog', 'Blog'),
        ('news', 'News')
)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        for post in Post.objects.filter(author=self.user):
            self.rating += post.rating*3
        for comment in Comment.objects.filter(author=Comment.post):
            self.rating += comment.rating
        for comment in Comment.objects.filter(author=Comment.user):
            self.rating += comment.rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=255, choices=blog_news_choice, default='blog')
    time_created = models.DateTimeField(auto_now_add=True, )
    category = models.ManyToManyField(Category, through='PostCategory')
    object_title = models.CharField(max_length=60, default='no title')  # max title length is 60
    object_content = models.TextField(default='no text')
    rating = models.IntegerField(default=0)

    def like(self,):
        self.rating += 1
        self.save()

    def dislike(self,):
        self.rating -= 1
        self.save()

    def preview(self,):
        self.object_content = self.object_content[0:125]+'...'
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default='no text')
    time_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self,):
        self.rating += 1
        self.save()

    def dislike(self,):
        self.rating -= 1
        self.save()
