from django.contrib.sitemaps import Sitemap
from .models import Add_Service

class ServiceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Add_Service.objects.all()

    def lastmod(self, obj):
        return obj.data_created
