from django.contrib import admin

# Register your models here.
from .models import CalendarEntry, Infohome, Link, LinkType

# Register your models here.
admin.site.register(CalendarEntry)
admin.site.register(Infohome)
admin.site.register(Link)
admin.site.register(LinkType)