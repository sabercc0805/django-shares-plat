from django import template
register = template.Library()

@register.filter
def division(value):
    return round((value / 10),1)