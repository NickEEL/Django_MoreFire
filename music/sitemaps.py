from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from mfevents.models import Mix, Track


class MixViewSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Mix.objects.all().order_by('-release_date')

    def lastmod(self, obj):
        return obj.release_date


class TrackViewSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Track.objects.all().order_by('-release_date')

    def lastmod(self, obj):
        return obj.release_date