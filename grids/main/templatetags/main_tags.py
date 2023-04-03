from django import template
from main.models import *

register = template.Library()


@register.simple_tag()
def get_product_by_id(product_id):
    product = PriceWinguardMain.objects.all()
    return product
