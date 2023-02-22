"""mfproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from home.sitemaps import StaticHomeViewSitemap, CalendarEntrySitemap
from music.sitemaps import MixViewSitemap, TrackViewSitemap
from mfevents.sitemaps import ListingsViewSitemap, PastEventsViewSitemap
from galleries.sitemaps import GalleryViewSitemap, PhotoViewSitemap


sitemaps= {
    'static_home': StaticHomeViewSitemap,
    'calendar_entry': CalendarEntrySitemap,
    'mix': MixViewSitemap,
    'track': TrackViewSitemap,
    'listings': ListingsViewSitemap,
    'pastevents': PastEventsViewSitemap,
    'gallery': GalleryViewSitemap,
    'photo': PhotoViewSitemap,

}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('home.urls')),
    path('events/', include('mfevents.urls')),
    path('music/', include('music.urls')),
    path('photos/', include('galleries.urls')),
    path('captcha/', include('captcha.urls')),
    path("django-check-seo/", include("django_check_seo.urls")),
]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # below if statements used when setting up S3. Removethis line if successful

if settings.LOCAL_SERVE_STATIC_FILES:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.LOCAL_SERVE_MEDIA_FILES:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
