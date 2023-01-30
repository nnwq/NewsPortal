from django_filters import *
import django_filters
from .models import Post, Category
from django import forms


class NewsFilter(FilterSet):

    post_type = django_filters.ChoiceFilter(choices=Post.post_type, label="Post type ", lookup_expr='iexact')
    creation = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                                         label="Created ", lookup_expr='date__gt')
    category = django_filters.ChoiceFilter(choices=[[c.id] for c in Category.objects.all().order_by('category_name')], label="News Category ")


    class Meta:
       model = Post
       fields = {
           'object_title': ['icontains'],
       }
