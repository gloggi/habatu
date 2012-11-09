from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import TemplateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from .models import Game
from .forms import GameForm, GameFormDND

admin.autodiscover()

urlpatterns = patterns('habatu.views',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

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
            template_name='habatu/saved.html'
        ), name="tournament_saved"),
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True
        }
    ),
)
