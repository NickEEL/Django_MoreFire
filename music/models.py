from django.db import models
from django.utils import timezone

# Create your models here.
class Genre(models.Model):
    name = models.CharField('Musical Genre Name', max_length=100, default='')

    def __str__(self):
        return self.name



class Soundsystem(models.Model):
    name = models.CharField('Sound Name', max_length=100, default='')
    genre = models.ManyToManyField(Genre, related_name='sound_genre')
    rank = models.IntegerField('Sound rank', )
    location = models.CharField('Location', max_length=250, blank=True, null=True)
    contact_name = models.CharField('Contact', max_length=50, blank=True, null=True)
    contact_phone = models.CharField('Contact phone number', max_length=15, blank=True, null=True)
    contact_email = models.EmailField('Email', blank=True, null=True)
    sound_url = models.URLField('weblink', blank=True, null=True)
    created_dt = models.DateTimeField('Date created', auto_now_add=True)
    edited_dt = models.DateTimeField('Date edited', auto_now=True)

    class Meta:
        ordering = ['rank', 'name',]

    def __str__(self):
        return self.name


class Band(models.Model):
    name = models.CharField('Band name', max_length=100, default='')
    genre = models.ManyToManyField(Genre, related_name='group_genre')
    rank = models.IntegerField('rank: Headline is low number')
    location = models.CharField('Location', max_length=250, blank=True, null=True)
    contact_name = models.CharField('Contact', max_length=50, blank=True, null=True)
    contact_phone = models.CharField('Contact phone number', max_length=15, blank=True, null=True)
    contact_email = models.EmailField('Email', blank=True, null=True)
    band_url = models.URLField('website', blank=True, null=True)
    created_dt = models.DateTimeField('Date created', auto_now_add=True)
    edited_dt = models.DateTimeField('Date edited', auto_now=True)

    class Meta:
        ordering = ['rank', 'name',]

    def __str__(self):
        return self.name



class Label(models.Model):
    name = models.CharField('Label Name', max_length=100, default='')
    location = models.CharField('Label location', max_length=250, blank=True, null=True)
    contact_name = models.CharField('Label contact', max_length=50, blank=True, null=True)
    contact_phone = models.CharField('Label phone number', max_length=15, blank=True, null=True)
    contact_email = models.EmailField('Label email', blank=True, null=True)
    website = models.URLField('Label web address', blank=True, null=True)
    created_dt = models.DateTimeField('Date created', auto_now_add=True)
    edited_dt = models.DateTimeField('Date edited', auto_now=True)

    def __str__(self):
        return self.name



class Studio(models.Model):
    name = models.CharField('Studio Name', max_length=100, default='')
    location = models.CharField('Studio location', max_length=250, blank=True, null=True)
    contact_name = models.CharField('Studio contact', max_length=50, blank=True, null=True)
    contact_phone = models.CharField('Studio phone number', max_length=15, blank=True, null=True)
    contact_email = models.EmailField('Studio email', blank=True, null=True)
    website = models.URLField('Studio web address', blank=True, null=True)
    created_dt = models.DateTimeField('Date created', auto_now_add=True)
    edited_dt = models.DateTimeField('Date edited', auto_now=True)

    def __str__(self):
        return self.name



class ArtistType(models.Model):
    name = models.CharField('Artist Type Name', max_length=100, default='')
    selecta = models.BooleanField('Selecta (DJ, CDJ etc.) = true', default=False)
    vocalist = models.BooleanField('Vocalist (MC; Singer; Beatbox etc.) = true', default=False)
    instrumentalist = models.BooleanField('Instrumentist (including electronic) = True', default=False)

    def __str__(self):
        return self.name



class Artist(models.Model):
    name = models.CharField('Artist Name', max_length=100, default='')
    artist_type = models.ManyToManyField(ArtistType, related_name='artist_type')
    genre = models.ManyToManyField(Genre, related_name='artist_genre')
    rank = models.IntegerField('rank: Headline is low number',)
    crew = models.ForeignKey(Soundsystem, on_delete=models.PROTECT, blank=True, null=True)
    band = models.ManyToManyField(Band, related_name='artist_bands')
    location = models.CharField('Artist Location', max_length=100, null=True, blank=True)
    email = models.EmailField('Artist Email', null=True, blank=True)
    artist_url = models.URLField('Artist Website', blank=True, null=True)
    created_dt = models.DateTimeField('Date created', auto_now_add=True)
    edited_dt = models.DateTimeField('Date edited', auto_now=True)

    class Meta:
        ordering = ['rank', 'name', ]

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField('Producer Name', max_length=100, default='')
    producer_location = models.CharField('Producer Location', max_length=100, null=True, blank=True)
    producer_email = models.EmailField('Producer Email', null=True, blank=True)
    producer_url = models.URLField('Producer Website', blank=True, null=True)
    created_dt = models.DateTimeField('Date created', auto_now_add=True)
    edited_dt = models.DateTimeField('Date edited', auto_now=True)

    def __str__(self):
        return self.name