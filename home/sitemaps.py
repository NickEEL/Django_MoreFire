from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import CalendarEntry


class StaticHomeViewSitemap(Sitemap):

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


class CalendarEntrySitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return CalendarEntry.objects.all()

    def lastmod(self, obj):
        return obj.created_dt