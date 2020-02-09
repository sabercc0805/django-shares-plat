from django import template
register = template.Library()

@register.filter
def division(value):
    return round((value / 10),1)

@register.filter
def div(value,div):
    return round((value / div),2)