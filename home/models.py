from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save


#from music.models import Track, Mix
from mfevents.models import MFEvent, Track, Mix


# Create your models here.
class Photohome(models.Model):
    name = models.CharField('Photo name', max_length=50, default='Photo #')
    hm_image = models.ImageField('Home page image', upload_to='home_images/', null=True, blank=True)
    portrait = models.BooleanField('Portrait? True/False', default=False)
    upload_dt = models.DateTimeField('Date Photo uploaded', auto_now_add=True)

    def __str__(self):
        return self.name


class Infohome(models.Model):
    headline = models.CharField('Headline', max_length=100, default='Headline')
    info = models.TextField('Home information', default='Write Text Here!')
    top = models.BooleanField('Top/welcome mesage (True/False)', default=False)
    created_dt = models.DateTimeField('Date created', auto_now_add=True)
    edited_dt = models.DateTimeField('Date edited', auto_now=True)
    mix = models.ForeignKey(Mix, on_delete=models.CASCADE, null=True, blank=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(MFEvent, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.headline


class LinkType(models.Model):
    name = models.CharField('Link type name', max_length=100, default='name')
    social = models.BooleanField('Social Media', default=False)
    stream = models.BooleanField('Music Streaming', default=False)
    radio = models.BooleanField('Radio', default=False)
    records = models.BooleanField('Records', default=False)
    ticket = models.BooleanField('Tickets', default=False)
    tek =  models.BooleanField('Technical Equipment', default=False)
    merch = models.BooleanField('Merchandise', default=False)
    culture = models.BooleanField('Culture', default=False)
    other = models.BooleanField('Other links', default=False)

    def __str__(self):
        return self.name



class Link(models.Model):
    name = models.CharField('Link name', max_length=100, default='name')
    linktype = models.ForeignKey(LinkType, on_delete=models.PROTECT, null=False)
    mflink = models.BooleanField('More Fire link', default=False)
    mix_bol = models.BooleanField('Mix link', default=False)
    track_bol = models.BooleanField('Track link', default=False)
    mix = models.ForeignKey(Mix, on_delete=models.CASCADE, null=True, blank=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True, blank=True)
    link_url = models.URLField('Link url')
    logo_lnk = models.ImageField('Link Logo', upload_to= 'logo_images/', null=True, blank=True)

    def __str__(self):

        if self.mflink==True and self.mix_bol==False and self.track_bol==False:
            return '%s (%s)' % (self.name, self.linktype)
        elif self.mix_bol:
            return '%s (%s)' % (self.mix, self.linktype)
        elif self.track_bol:
            return '%s (%s)' % (self.track, self.linktype)
        elif self.mflink==False and self.mix_bol==False and self.track_bol==False:
            return self.name
        else:
            Print('Error check booleans')



class CalendarEntry(models.Model):
    event_bol = models.BooleanField('Event True/False', default=False)
    mix_bol = models.BooleanField('Mix True/False', default=False)
    track_bol = models.BooleanField('Track True/False', default=False)
    date = models.DateField('Entrydate', null=True, blank=True)
    event = models.OneToOneField(MFEvent, on_delete=models.CASCADE, null=True, blank=True)
    mix = models.OneToOneField(Mix, on_delete=models.CASCADE, null=True, blank=True)
    track = models.OneToOneField(Track, on_delete=models.CASCADE, null=True, blank=True)
    created_dt = models.DateTimeField('Date created', auto_now_add=True)
    edited_dt = models.DateTimeField('Date edited', auto_now=True)

    def __str__(self):
        if self.event_bol:
            event = 'Event #%s' % (self.event.pk)
            return event
        elif self.mix_bol:
            mix = 'Mix #%s' % (self.mix.pk)
            return mix
        elif self.track_bol:
            track = 'Track #%s' % (self.track.pk)
            return track
        else:
            print("Error: Checkeck Booleans")


    @property
    def start_date(self):
        e = self.event_bol
        m = self.mix_bol
        t = self.track_bol
        st_date = ''
        if e:
            st_date = self.event.start_dt
        elif m:
            st_date = self.mix.release_date
        elif t:
            st_date = self.track.release_date
        else:
            Print("Error: Check dates or booleans!")
        return st_date

    @property
    def finish_date(self):
        e = self.event_bol
        m = self.mix_bol
        t = self.track_bol
        fn_date = ''
        if e:
            fn_date = self.event.finish_dt
        elif m:
            fn_date = self.mix.release_date
        elif t:
            fn_date = self.track.release_date
        else:
            Print("Error: Check dates or booleans!")
        return fn_date


    def get_absolute_url(self):
        n = '' # sets the name url variable name
        k = {} # sets the kwargs variable
        if self.event_bol == True:
            n = 'event-profile'
            k = {'event_id': self.event.id}
        elif self.mix_bol == True:
            n = 'mix-profile'
            k = {'mix_id': self.mix.id}
        elif self.track_bol == True:
            n = 'track_profile'
            k = {'track_id': self.track.id}
        else:
            Print("Error: Booleans boxes not correct, check if 0 or >1 boxes checked!")

        return reverse(n, kwargs=k)


def create_entry(sender, **kwargs):
    if kwargs['created']:
        if sender == MFEvent:
            entry = CalendarEntry.objects.create(
                event_bol=True,
                date=kwargs['instance'].start_dt,
                event=kwargs['instance'],
            )
        elif sender == Mix:
            entry = CalendarEntry.objects.create(
                mix_bol=True,
                date=kwargs['instance'].release_date,
                mix=kwargs['instance'],
            )
        elif sender == Track:
            entry = CalendarEntry.objects.create(
                track_bol=True,
                date=kwargs['instance'].release_date,
                track=kwargs['instance'],
            )
        else:
            print("Error: somethings up!")


post_save.connect(create_entry, sender= MFEvent)
post_save.connect(create_entry, sender= Mix)
post_save.connect(create_entry, sender= Track)
