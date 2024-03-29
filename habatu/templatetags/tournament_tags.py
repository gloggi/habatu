from django import template

register = template.Library()

from ..models import Game


@register.inclusion_tag('habatu/_gameslot.html')
def render_slot(timeframe, location):

    slot_id = u"%s_%s" % (timeframe.id, location.id)
    games = Game.objects.filter(time=timeframe, location=location)

    return {
        'timeframe': timeframe,
        'location': location,
        'slot_id': slot_id,
        'games': games,
    }


@register.inclusion_tag('habatu/_slotview.html')
def render_slot_view(timeframe, location):

    slot_id = u"%s_%s" % (timeframe.id, location.id)
    games = Game.objects.filter(time=timeframe, location=location)

    return {
        'timeframe': timeframe,
        'location': location,
        'slot_id': slot_id,
        'games': games,
    }


@register.inclusion_tag('habatu/_game.html')
def render_game(game):

    return {
        'game': game,
    }


@register.inclusion_tag('habatu/_lunchtime.html')
def render_lunch_time(timeframe):

    end = timeframe.end

    its_lunch_time = end.hour == 12 and end.minute == 00

    print end

    return {
        'should_render': its_lunch_time
    }
