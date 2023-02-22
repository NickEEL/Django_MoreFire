from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Gallery, Photo

class GalleryViewSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Gallery.objects.all()

    def lastmod(self, obj):
        return obj.created_dt


class PhotoViewSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Photo.objects.all()

    def lastmod(self, obj):
        return obj.created_dt
