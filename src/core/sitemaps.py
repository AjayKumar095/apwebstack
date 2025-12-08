from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return [
            'index',               # /
            'contact',             # /contact/
            'terms_of_use',        # /policy/terms-of-use/
            'about_us'
        ]

    def location(self, item):
        return reverse(item)
