from django.core.management.base import NoArgsCommand

from datetime import datetime, timedelta

from ...models import Timeframe


class Command(NoArgsCommand):
    help = 'Closes the specified poll for voting'

    def handle_noargs(self, **options):
        print "Creating timeframes..."

        start_time = datetime(year=2013, month=11, day=3, hour=9, minute=30)

        game_duration = timedelta(minutes=15)

        # morning games
        launch_time = datetime(year=2013, month=11, day=3, hour=12, minute=00)

        while start_time < launch_time:
            fr = Timeframe.objects.get_or_create(
                start=start_time,
                end=start_time + game_duration
            )
            start_time += game_duration
            print fr

        # 1 hour lunch!
        start_time += timedelta(minutes=60)

        #
        end_time = datetime(year=2013, month=11, day=3, hour=17, minute=00)

        while start_time < end_time:
            fr = Timeframe.objects.get_or_create(
                start=start_time,
                end=start_time + game_duration
            )
            start_time += game_duration
            print fr
