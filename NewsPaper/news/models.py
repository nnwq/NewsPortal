from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)


class Category(models.Model):


class Post(models.Model):


class PostCategory(models.Model):


class Comment(models.Model):
