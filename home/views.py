from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from datetime import datetime, date, timedelta
import pytz
from pytz import timezone
from django.utils.safestring import mark_safe
import calendar
from calendar import HTMLCalendar
from .calendar import MFCalendar
from .models import CalendarEntry
from itertools import chain
from .models import Photohome, Infohome, Link
from music.models import  Artist, Soundsystem, Studio, Producer, Label, Band
from mfevents.models import MFEvent, Venue, EventCrew, Mix, Track
from galleries.models import Gallery, Photo

#global variables
tz_uk = timezone('Europe/London')
tz_utc = pytz.utc
now_utc = datetime.now(timezone(tz_utc.zone))

current_year_utc = now_utc.year
# current month
current_month_utc = now_utc.month
# current day
current_day_utc = now_utc.day
# Get current time
current_time_utc = now_utc.strftime('%I:%M %p on %d.%m.%Y. %Z')

mf_entries_all = CalendarEntry.objects.exclude(event__status='Plan').exclude(event__status='Cancelled',
                                                                                  event__finished=True).order_by('date')
mf_ents_first_dt = None
mf_ents_last_dt = None
#Previous & Next month calculation
cal_month_name_lst = list(calendar.month_name)



# logic for first mf entry date
def first_entry_date(entries):
    mf_ents_first_dt = None
    mf_ents_first = entries.first()

    if mf_ents_first is not None:
        if mf_ents_first.event_bol:
            mf_ents_first_dt = mf_ents_first.event.start_dt
            return mf_ents_first_dt
        elif mf_ents_first.mix_bol:
            mf_ents_first_dt = mf_ents_first.mix.release_date
            return mf_ents_first_dt
        elif mf_ents_first.track_bol:
            mf_ents_first_dt = mf_ents_first.track.release_date
            return mf_ents_first_dt
        else:
            print('No first date returned')
    else:
        return now_utc



# logic for last mf entry date
def last_entry_date(entries):
    mf_ents_last_dt = None
    mf_ents_last = entries.last()

    if mf_ents_last is not None:
        if mf_ents_last.event_bol:
            mf_ents_last_dt = mf_ents_last.event.start_dt
            return mf_ents_last_dt
        elif mf_ents_last.mix_bol:
            mf_ents_last_dt = mf_ents_last.mix.release_date
            return mf_ents_last_dt
        elif mf_ents_last.track_bol:
            mf_ents_last_dt = mf_ents_last.track.release_date
            return mf_ents_last_dt
        else:
            print('No last date returned')
    else:
        return now_utc


# Create your views here.
def linksview(request):
    links_all = Link.objects.all()
    links_mf = Link.objects.filter(mflink=True).exclude(mix_bol=True).exclude(track_bol=True).order_by('name')
    links_social = Link.objects.filter(linktype__social=True).exclude(mflink=True).order_by('name')
    links_stream = Link.objects.filter(linktype__stream=True).exclude(mflink=True).order_by('name')
    links_records = Link.objects.filter(linktype__records=True).exclude(mflink=True).order_by('name')
    links_radio = Link.objects.filter(linktype__radio=True).exclude(mflink=True).order_by('name')
    links_ticket = Link.objects.filter(linktype__ticket=True).exclude(mflink=True).order_by('name')
    links_tek = Link.objects.filter(linktype__tek=True).exclude(mflink=True).order_by('name')
    links_merch = Link.objects.filter(linktype__merch=True).exclude(mflink=True).order_by('name')
    links_culture = Link.objects.filter(linktype__culture=True).exclude(mflink=True).order_by('name')
    links_other = Link.objects.filter(linktype__other=True).exclude(mflink=True).order_by('name')
    venues_all = Venue.objects.exclude(name='N/A').exclude(website__isnull=True).order_by('name')
    artists_all = Artist.objects.exclude(name='N/A').exclude(artist_url__isnull=True).order_by('name')
    soundsystem_all = Soundsystem.objects.exclude(name='N/A').exclude(name='More Fire Sound').exclude(sound_url__isnull=True).order_by('name')
    studio_all = Studio.objects.exclude(name='N/A').exclude(website__isnull=True).order_by('name')
    eventcrew_all = EventCrew.objects.exclude(name='N/A').exclude(name='More Fire').exclude(website__isnull=True).order_by('name')
    producers = Producer.objects.exclude(name='N/A').exclude(producer_url__isnull=True).order_by('name')
    labels = Label.objects.exclude(name='N/A').exclude(website__isnull=True).order_by('name')
    bands = Band.objects.exclude(name='N/A').exclude(band_url__isnull=True).order_by('name')

    args = {
        'current_year': current_year_utc,
        'links': links_all,
        'links_mf': links_mf,
        'links_social': links_social,
        'links_stream': links_stream,
        'links_records': links_records,
        'links_radio': links_radio,
        'links_ticket': links_ticket,
        'links_tek': links_tek,
        'links_culture': links_culture,
        'links_merch': links_merch,
        'links_other': links_other,
        'venues': venues_all,
        'artists_all':  artists_all,
        'soundsystem_all': soundsystem_all,
        'studio_all': studio_all,
        'eventcrew_all': eventcrew_all,
        'producers': producers,
        'labels': labels,
        'bands': bands,
    }

    return render(request, 'home/links.html', args)


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request):
        photo_hm = Photohome.objects.all()
        photo_hm_1st_rdm = Photohome.objects.order_by('?').first()
        links_mf = Link.objects.exclude(mflink=False).filter(linktype__social=True).order_by('name')
        links_mf_stream = Link.objects.filter(mflink=True).filter(linktype__stream=True).exclude(mix_bol=True).exclude(track_bol=True).order_by('name')
        try:
            info_hm_top = Infohome.objects.get(top=True)
        except:
            info_hm_top = None

        info_hm_xtop = Infohome.objects.exclude(top=True).order_by('-edited_dt')[:5]

        args = {
            'current_year': current_year_utc,
            'photo_hm': photo_hm_1st_rdm,
            'info_hm_top' : info_hm_top,
            'info_hm_xtop': info_hm_xtop,
            'links_mf': links_mf,
            'links_mf_stream': links_mf_stream,
        }
        return render(request, self.template_name, args)


def basearg(request):

    args = {
        'current_year': current_year_utc,
    }
    return render(request, 'base.html', args )



def hmcalendar(request, year=current_year_utc, month=current_month_utc):
    mf_entries = CalendarEntry.objects.order_by('date').filter(
        date__year=year, date__month=month).exclude(event__status='Plan').exclude(event__status='Cancelled',
                                                                                  event__finished=True)

    cal = MFCalendar(mf_entries).formatmonth(year, month)
    d = datetime.now(tz_uk)

    #Previous month
    first = d.replace(day=1)
    prev_month_last_day = first - timedelta(days=1)
    prev_month_num = prev_month_last_day.month
    prev_month = cal_month_name_lst[prev_month_num]
    prev_month_year_num = prev_month_last_day.year
    #Previous year
    d365_ago = d - timedelta(days=365)
    prev_yr_mon_num = d365_ago.month
    prev_yr_mon = cal_month_name_lst[prev_yr_mon_num]
    prev_yr = d365_ago.year
    #Oldest
    mf_ents_first_date = first_entry_date(mf_entries_all)
    mf_ents_first_yr = mf_ents_first_date.year
    mf_ents_first_mon_num = mf_ents_first_date.month
    mf_ents_first_mon = cal_month_name_lst[mf_ents_first_mon_num]

    #Next month
    days_in_month = calendar.monthrange(d.year, d.month)[1] # returns the number of days in the specified month.
    last = d.replace(day=days_in_month)
    next_month_day = last + timedelta(days=1)
    next_month_num = next_month_day.month
    next_month = cal_month_name_lst[next_month_num]
    next_month_year_num = next_month_day.year
    #Next year
    d365_plus = d + timedelta(days=365)
    next_yr_mon_num = d365_plus.month
    next_yr_mon = cal_month_name_lst[next_yr_mon_num]
    next_yr = d365_plus.year
    #Newest
    mf_ents_last_date = last_entry_date(mf_entries_all)
    mf_ents_last_yr = mf_ents_last_date.year
    mf_ents_last_mon_num = mf_ents_last_date.month
    mf_ents_last_mon = cal_month_name_lst[mf_ents_last_mon_num]


    args = {
        'current_year': current_year_utc,
        'calendar': mark_safe(cal),
        'prev_month': prev_month,
        'prev_month_year': prev_month_year_num,
        'prev_yr_mon': prev_yr_mon,
        'prev_yr': prev_yr,
        'next_month': next_month,
        'next_month_year': next_month_year_num,
        'next_yr_mon': next_yr_mon,
        'next_yr': next_yr,
        'mf_ents_1st_yr': mf_ents_first_yr,
        'mf_ents_1st_mon': mf_ents_first_mon,
        'mf_ents_last_yr': mf_ents_last_yr,
        'mf_ents_last_mon': mf_ents_last_mon,
    }
    return render(request,'home/calendar.html', args)


def hmcalendarchangeview(request, year, month):
    #variables
    month = month.capitalize()
    month_number = int(list(calendar.month_name).index(month))
    month_number = int(month_number)

    #Current datetime info
    now = datetime.now(tz_uk)
    # Get current year
    current_year = now.year
    # current month
    current_month = now.month
    # current day
    current_day = now.day
    # Get current time
    current_time = now.strftime('%I:%M %p on %d.%m.%Y. %Z')

    #More Fire Events
    mf_entries = CalendarEntry.objects.order_by('date').filter(
        date__year=year, date__month=month_number).exclude(event__status='Plan').exclude(event__status='Cancelled', event__finished=True )

    cal = MFCalendar(mf_entries).formatmonth(year, month_number)

    # Previous & Next month calculation
    cal_month_name_lst = list(calendar.month_name)

    d = date(year=year, month=month_number, day=15)

    # Previous
    first = d.replace(day=1)
    prev_month_last_day = first - timedelta(days=1)
    prev_month_num = prev_month_last_day.month
    prev_month = cal_month_name_lst[prev_month_num]
    prev_month_year_num = prev_month_last_day.year
    # Previous year
    d365_ago = d - timedelta(days=365)
    prev_yr_mon_num = d365_ago.month
    prev_yr_mon = cal_month_name_lst[prev_yr_mon_num]
    prev_yr = d365_ago.year
    # Oldest
    mf_ents_first_date = first_entry_date(mf_entries_all)
    mf_ents_first_yr = mf_ents_first_date.year
    mf_ents_first_mon_num = mf_ents_first_date.month
    mf_ents_first_mon = cal_month_name_lst[mf_ents_first_mon_num]
    # Next month
    days_in_month = calendar.monthrange(d.year, d.month)[1]  # returns the number of days in the specified month.
    last = d.replace(day=days_in_month)
    next_month_day = last + timedelta(days=1)
    next_month_num = next_month_day.month
    next_month = cal_month_name_lst[next_month_num]
    next_month_year_num = next_month_day.year
    # Next year
    d365_plus = d + timedelta(days=365)
    next_yr_mon_num = d365_plus.month
    next_yr_mon = cal_month_name_lst[next_yr_mon_num]
    next_yr = d365_plus.year
    #Newest
    mf_ents_last_date = last_entry_date(mf_entries_all)
    mf_ents_last_yr = mf_ents_last_date.year
    mf_ents_last_mon_num = mf_ents_last_date.month
    mf_ents_last_mon = cal_month_name_lst[mf_ents_last_mon_num]

    #arguments for template
    args = {
        'year':year,
        'month':month,
        'month_number':month_number,
        'current_year': current_year,
        'current_month': current_month,
        'current_day': current_day,
        'current_time': current_time,
        'mf_entries': mf_entries,
        'calendar': mark_safe(cal),
        'prev_month': prev_month,
        'prev_month_year': prev_month_year_num,
        'next_month': next_month,
        'next_month_year': next_month_year_num,
        'prev_yr_mon': prev_yr_mon,
        'prev_yr': prev_yr,
        'next_yr_mon': next_yr_mon,
        'next_yr': next_yr,
        'mf_ents_1st_yr': mf_ents_first_yr,
        'mf_ents_1st_mon': mf_ents_first_mon,
        'mf_ents_last_yr': mf_ents_last_yr,
        'mf_ents_last_mon': mf_ents_last_mon,
    }
    return render(request, 'home/calendar_change.html', args)


def site_search(request):
    #Check if events have finished
    events_list_all = MFEvent.objects.all()
    for e in events_list_all:
        if e.finish_dt < now_utc:
            e.finished = True
            e.save()

    if request.method == "POST":
        searched = request.POST['searched']
        #Q query expressions
        events_q = Q(name__icontains=searched) | Q(venue__name__icontains=searched) | Q(selectas__name__icontains=searched) | Q(vocals__name__icontains=searched) | Q(instrumentals__name__icontains=searched) | Q(genre__name__icontains=searched)
        mix_q = Q(name__icontains=searched) | Q(dj__name__icontains=searched) | Q(featured_artists__name__icontains=searched) | Q(genre__name__icontains=searched)
        track_q = Q(name__icontains=searched) | Q(producer__name__icontains=searched) | Q(featured_artists__name__icontains=searched) | Q(label__name__icontains=searched) | Q(studio__name__icontains=searched) | Q(genre__name__icontains=searched)
        galleries_q = Q(name__icontains=searched) | Q(event__name__icontains=searched)
        photo_q = Q(name__icontains=searched)

        #Search filters
        listings_srch = MFEvent.objects.filter(events_q).exclude(status='Plan').exclude(finished=True).order_by('start_dt').distinct()
        past_events_srch = MFEvent.objects.filter(events_q).exclude(status='Plan').exclude(finished=False).order_by('start_dt').distinct()
        mix_srch = Mix.objects.filter(mix_q).order_by('release_date').distinct()
        track_srch = Track.objects.filter(track_q).order_by('release_date').distinct()
        galleries_srch = Gallery.objects.filter(galleries_q).order_by('created_dt').distinct()
        photo_srch = Photo.objects.filter(photo_q).order_by('created_dt').distinct()



        #Search Counts
        listing_srch_count = len(listings_srch)
        past_events_srch_count = len(past_events_srch)
        mix_srch_count = len(mix_srch)
        track_srch_count = len(track_srch)
        galleries_srch_count = len(galleries_srch)
        photo_srch_count = len(photo_srch)

        total_srch_counts = sum([
            listing_srch_count,
            past_events_srch_count,
            mix_srch_count,
            track_srch_count,
            galleries_srch_count,
            photo_srch_count,
            ])


        args = {
            'current_year': current_year_utc,
            'searched': searched,
            'listings_srch': listings_srch,
            'past_events_srch': past_events_srch,
            'mix_srch': mix_srch,
            'track_srch': track_srch,
            'galleries_srch': galleries_srch,
            'photo_srch': photo_srch,
            'listing_srch_count': listing_srch_count,
            'past_events_srch_count': past_events_srch_count,
            'mix_srch_count': mix_srch_count,
            'track_srch_count': track_srch_count,
            'galleries_srch_count': galleries_srch_count,
            'photo_srch_count': photo_srch_count,
            'total_srch_counts': total_srch_counts,
            }

        return render(request, 'home/site_search.html', args)
    else:
        return render(request, 'home/site_search.html')

