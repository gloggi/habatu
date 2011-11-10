from django.conf import settings


def tournament_settings(context):
    return {'TOURNAMENT_TITLE': settings.TOURNAMENT_TITLE,
            'TOURNAMENT_LOGO': settings.TOURNAMENT_LOGO,
            'SCHEDULE_MODE': settings.SCHEDULE_MODE,}