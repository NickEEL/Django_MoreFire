from django.db import models
from mfevents.models import MFEvent
from django.urls import reverse

# Create your models here.

class Gallery(models.Model):
    name = models.CharField('Gallery name', max_length=50)
    event = models.ForeignKey(MFEvent, on_delete=models.CASCADE, null=True, blank=True)
    created_dt = models.DateTimeField('Date created', auto_now_add=True)
    edited_dt = models.DateTimeField('Date edited', auto_now=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField('Photo name', max_length=50, default='Photo')
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    cover = models.BooleanField('Gallery cover? True/False', default=False)
    photo = models.ImageField('Photo', upload_to='photos/', null=True)
    portrait = models.BooleanField('Portrait? True/False', default=False)
    info = models.TextField('Photo info.', null=True, blank=True)
    created_dt = models.DateTimeField('Date created', auto_now_add=True)
    edited_dt = models.DateTimeField('Date edited', auto_now=True)

    def __str__(self):
        return '%s #%s (%s)' % (self.name, self.pk, self.gallery)

    def get_absolute_url(self):
        k = {'gallery': self.gallery, 'photo_id': self.id}
        return reverse('photo', kwargs=k)
