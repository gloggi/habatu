from django.conf.urls.defaults import *

urlpatterns =  patterns('django_tournament.tournament.views',
    url(r'^$', 'table_view', name="tournament_table"),
    url(r'^edit/$', 'table_edit', name="tournament_table"),
    url(r'^stats/$', 'stats', name="tournament_stats"),
    url(r'^create/$', 'game_create', name="tournament_game_create"),
    url(r'^create/(?P<timeframe_id>\d+)/(?P<location_id>\d+)/', 'game_create_direct', \
        name="tournament_game_create_direct"),
    url(r'^gamecount/$', 'game_count', name="tournament_game_count"),
    url(r'^update/(?P<id>\d+)/$', 'game_update', name="tournament_game_update"),
    url(r'^delete/(?P<id>\d+)/$', 'game_delete', name="tournament_game_delete"),
)

urlpatterns +=  patterns('django.views.generic.simple',
    (r'^saved/$', 'direct_to_template', {'template': 'tournament/game_saved.html'},
      "tournament_game_saved"),
)