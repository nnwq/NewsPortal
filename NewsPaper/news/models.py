from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    def update_rating(self):
        return


class Category(models.Model):


class Post(models.Model):
    def like(self,):

        return
    def dislike(self,):
        return

    def preview(self,):
        return


class PostCategory(models.Model):



class Comment(models.Model):
    def like(self,):
        return
    def dislike(self,):
        return