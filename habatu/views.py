from django.shortcuts import render
from django.views.generic.create_update import create_object
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect


from models import Tournament, Team, Timeframe, Location, Game
from forms import GameForm


def table_edit(request):
    locations = Location.objects.all()
    timeframes = Timeframe.objects.all()
    teams = Team.objects.filter(tournament__hidden=False)
    tournaments = Tournament.objects.filter(hidden=False)

    return render(request, 'habatu/table_edit.html', {
        'locations': locations,
        'timeframes': timeframes,
        'teams': teams,
        'tournaments': tournaments,
    })


def table_view(request):
    locations = Location.objects.all()
    timeframes = Timeframe.objects.all()
    teams = Team.objects.filter(tournament__hidden=False)
    tournaments = Tournament.objects.filter(hidden=False)

    return render(request, 'habatu/table_view.html', {
        'locations': locations,
        'timeframes': timeframes,
        'teams': teams,
        'tournaments': tournaments,
    })


def stats(request):
    tournaments = Tournament.objects.filter(hidden=False).select_related()

    return render(request, 'habatu/stats.html', {
        'tournaments': tournaments
    })


def game_create(request):
    return create_object(request,
        model=Game,
        post_save_redirect=reverse('tournament_game_saved')
    )


def game_create_direct(request, timeframe_id, location_id):
    timeframe = get_object_or_404(Timeframe, pk=timeframe_id)
    location = get_object_or_404(Location, pk=location_id)

    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tournament_saved')
    else:
        form = GameForm(initial={
            'time': timeframe,
            'location': location,

        })

    return render(request, 'habatu/game_form.html', {
        'form': form,
    })


def game_count(request):

    tournaments = Tournament.objects.exclude(pk=4).select_related()

    return render(request, 'habatu/game_count.html', {
        'tournaments': tournaments
    })