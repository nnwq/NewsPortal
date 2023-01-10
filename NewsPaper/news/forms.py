from django.db import forms

blog_news_choice = (
        ('blog', 'Blog'),
        ('news', 'News')
)


class BlogNewsChoice(forms.Form):
    choice_field = forms.ChoiceField(choices=blog_news_choice)
