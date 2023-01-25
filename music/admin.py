from django.contrib import admin
from .models import Artist, ArtistType, Genre, Band, Producer, Soundsystem, Label, Studio

# Register your models here.
admin.site.register(ArtistType)
admin.site.register(Genre)
admin.site.register(Band)
admin.site.register(Label)
admin.site.register(Producer)
admin.site.register(Soundsystem)
admin.site.register(Studio)

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name','email' )
    ordering = ('name',)
#admin.site.register(Artist)
