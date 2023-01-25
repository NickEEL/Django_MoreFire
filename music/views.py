from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator

from .models import Artist, Label
from mfevents.models import Mix, Track
from home.models import Link

# Global datetime variable.
now = timezone.now()
current_year = now.year

# Create your views here.
def music_mix_profile(request, mix_id):
    mix_profile = Mix.objects.get(pk=mix_id)
    feat_artists = mix_profile.featured_artists.exclude(name='N/A')
    genre = mix_profile.genre.exclude(name='N/A')
    event = mix_profile.event
    links = Link.objects.filter(mix=mix_id).filter(mix_bol=True).order_by('name')

    args = {
        'mix_profile': mix_profile,
        'feat_artists': feat_artists,

        'genre': genre,
        'event': event,
        'links': links,
        'current_year': current_year,
    }
    return render(request, 'music/music_mix_profile.html', args)


def music_track_profile(request, track_id):
    track_profile = Track.objects.get(pk=track_id)
    feat_artists = track_profile.featured_artists.exclude(name='N/A')
    feat_artists_vl = track_profile.featured_artists.exclude(name='N/A').values_list('name', 'artist_url')
    band = track_profile.band
    studio = track_profile.studio
    producer = track_profile.producer.exclude(name='N/A').order_by('name')
    genre = track_profile.genre.exclude(name='N/A')
    links = Link.objects.filter(track=track_id)

    args = {
        'track_profile': track_profile,
        'feat_artists': feat_artists,
        'feat_artists_vl': feat_artists_vl,
        'producer': producer,
        'band': band,
        'studio': studio,
        'genre': genre,
        'links': links,
        'current_year': current_year,
    }
    return render(request, 'music/music_track_profile.html', args)



def music_mixes(request):

    mix_list_all= Mix.objects.all().order_by('-release_date')

    # pagination
    p = Paginator(mix_list_all, 5)
    page = request.GET.get('page')
    mix_list_page = p.get_page(page)
    nums = "p" * mix_list_page.paginator.num_pages

    args = {
        'mix_list_all': mix_list_all,
        'mix_list_page': mix_list_page,
        'nums': nums,
        'current_year': current_year,
    }

    return render(request, 'music/music_mixes.html', args)


def music_tracks(request):

    track_list_all = Track.objects.all().order_by('-release_date')

    # pagination
    p = Paginator(track_list_all, 5)
    page = request.GET.get('page')
    track_list_page = p.get_page(page)
    nums = "p" * track_list_page.paginator.num_pages

    args = {
        'track_list_all': track_list_all,
        'track_list_page': track_list_page,
        'nums': nums,
        'current_year': current_year,
    }

    return render(request, 'music/music_tracks.html', args)
