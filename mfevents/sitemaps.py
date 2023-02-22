from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import MFEvent

class ListingsViewSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return MFEvent.objects.exclude(status='Plan').exclude(finished=True).order_by('start_dt')

    def lastmod(self, obj):
        return obj.edited_dt


class PastEventsViewSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return MFEvent.objects.filter(finished=True).filter(status='Scheduled').order_by('-finish_dt')

    def lastmod(self, obj):
        return obj.edited_dt
