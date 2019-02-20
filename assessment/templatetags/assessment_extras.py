from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def backslash(value):
    if isinstance(value, str):
        return value.replace("\\", "\\\\")
    else:
        raise ValueError()


@register.filter
def my_range(value):
    if isinstance(value, int):
        return range(value)
    else:
        raise ValueError()


@register.filter
def my_range5(value):
    if isinstance(value, int):
        value = 5 - value
        return range(value)
    else:
        raise ValueError()
