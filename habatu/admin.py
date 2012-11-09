from django.contrib import admin

from models import Tournament, Team, Timeframe, Location, Game

admin.site.register(Tournament)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'club', 'tournament')

admin.site.register(Team, TeamAdmin)
admin.site.register(Timeframe)
admin.site.register(Location)
admin.site.register(Game)

