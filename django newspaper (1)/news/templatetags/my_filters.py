from django import template

register = template.Library()


@register.filter(name='Censor')
def Censor(value):
    if value == 'Fuck':
        return value == '****'
    else:
        return value