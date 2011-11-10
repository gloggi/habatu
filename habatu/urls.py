from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^django_tournament/', include('django_tournament.foo.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^tour/', include('django_tournament.tournament.urls')),
)

urlpatterns +=  patterns('django.views.generic.simple',
    #(r'^$', 'direct_to_template', {'template': 'base.html'}),
)

import sys
from django.conf import settings
if 'runserver' in sys.argv:
    urlpatterns += patterns('django.views.static', 
        (r'^media/(?P<path>.*)$', 'serve', {
                'document_root': settings.MEDIA_ROOT, 
                'show_indexes':True
            }
        ),
      
    )