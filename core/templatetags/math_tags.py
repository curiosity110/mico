from django import template

register = template.Library()


@register.filter(name="multiply")
def multiply(value, arg):
    """
    Multiplies the value by the given argument.
    Usage in template: {{ some_value|multiply:3 }}
    """
    return value * arg
