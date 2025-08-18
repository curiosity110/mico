from django import template

register = template.Library()

@register.filter
def currency(value, suffix="mkd"):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value
    return f"{value:.2f} {suffix}"
