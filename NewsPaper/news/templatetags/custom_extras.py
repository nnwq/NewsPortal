from django import template
from datetime import datetime


register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


forbidden_words = ['___', '____']


@register.filter
def hide_forbidden(value):
    words = value.slpit()
    result = []
    for word in words:
        if word in forbidden_words:
            result.append(word[0]+"*"*(len(word)-2)+word[-1])
        else:
            result.append(word)
    return "".join(result)


