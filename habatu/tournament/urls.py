from django.conf.urls.defaults import *

from django.views.generic import TemplateView , UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from forms import GameForm, GameFormDND
from models import Game

urlpatterns =  patterns('habatu.tournament.views',
    url(r'^$', 'table_view', name="tournament_table"),
    url(r'^edit/$', 'table_edit', name="tournament_edit"),
    url(r'^stats/$', 'stats', name="tournament_stats"),
    url(r'^create/$', 'game_create', name="tournament_game_create"),
    url(r'^create/(?P<timeframe_id>\d+)/(?P<location_id>\d+)/', \
        'game_create_direct', name="tournament_game_create_direct"),
    url(r'^gamecount/$', 'game_count', name="tournament_game_count"),
    url(r'^update/(?P<pk>\d+)/$', UpdateView.as_view(
            model=Game,
            form_class=GameForm,
            success_url='/saved/',
        ), name="tournament_game_update"),
    url(r'^update_dnd/(?P<pk>\d+)/$', csrf_exempt(UpdateView.as_view(
            model=Game,
            form_class=GameFormDND,
            success_url='/saved/',
        )), name="tournament_game_update_dnd"),
    url(r'^delete/(?P<pk>\d+)/$', DeleteView.as_view(
            model=Game,
            success_url='/saved/'
        ), name="tournament_game_delete"),
    url(r'^saved/$', TemplateView.as_view(
            template_name='tournament/saved.html'
        ), name="tournament_saved"),
)
