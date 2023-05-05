from django import template
from main.views import get_paginated_url

register = template.Library()

@register.simple_tag
def paginated_url(request, page):
    return get_paginated_url(request, page)
