from django import template

register = template.Library()

@register.filter(name="spaced_format")
def spaced_format(value):
    left = str(int(value / 1000))
    right = str(value % 1000).zfill(3)
    formatted_number = left + ' ' + right
    return formatted_number
