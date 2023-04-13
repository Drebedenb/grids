import re
from django import template
from main.models import *

register = template.Library()


@register.simple_tag()
def get_product_by_id(sketch_id):
    if not sketch_id:
        return None
    product = {}
    path = "".join(
        re.findall("\/\d+\/\d+", PriceWinguardFiles.objects.get(price_winguard_sketch_id=sketch_id).path))
    path_arr = path.split("/")
    product["path_folder"] = path_arr[1]
    product["path_file"] = path_arr[2]
    product['additional_info'] = list(
        PriceWinguardMain.objects.filter(price_winguard_sketch_id=sketch_id).values('price_b2c', 'name'))
    return product
