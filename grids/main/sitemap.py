from django.contrib.sitemaps import Sitemap
from .models import PriceWinguardMain

class PriceWinguardMainSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return PriceWinguardMain.objects.all

    def lastmod(self, obj):
        return obj.pub_date