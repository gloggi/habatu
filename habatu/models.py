from django.db import models
from django.utils.translation import ugettext_lazy as _


def compare_teams(teamA, teamB):
    if (teamA.points == teamB.points):
        if teamA.score_ratio() > teamB.score_ratio():
            return -1
        else:
            return 1
    else:
        return teamB.points - teamA.points


class Tournament(models.Model):
    title = models.CharField(_('title'), max_length=100)
    hidden = models.BooleanField(_('hidden'),
        help_text=_('dont show in result table'))

    class Meta:
        ordering = ('id',)
        verbose_name = _('Tournament')
        verbose_name_plural = _('Tournaments')

    def __unicode__(self):
        return self.title

    def teams_by_rank(self):
        return sorted(self.team_set.all(), cmp=compare_teams)


class Team(models.Model):
    name = models.CharField(_('name'), max_length=100)
    manager = models.CharField(_('manager'), max_length=100,
        blank=True, null=True)
    club = models.CharField(_('club'), max_length=100,
        blank=True, null=True)
    tournament = models.ForeignKey(Tournament)

    class Meta:
        ordering = ('tournament',)
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')

    def __unicode__(self):
        return self.name

    def all_games(self):
        return self.games_a.all() | self.games_b.all()

    def total_games(self):
        return self.all_games().count()

    def games_played(self):
        return len([g for g in self.all_games() if g.is_finished])

    def total_goals_shot(self):
        return sum([g.goals_shot(self) for g in self.all_games()])

    def total_goals_received(self):
        return sum([g.goals_received(self) for g in self.all_games()])

    def score_ratio_display(self):
        scored = self.total_goals_shot()
        received = self.total_goals_received()
        return "%d : %d" % (scored, received)

    def score_ratio(self):
        scored = self.total_goals_shot()
        received = self.total_goals_received()
        return float(scored) / (float(received) + 0.00001)

    @property
    def points(self):
        points = 0
        for game in self.all_games():
            if game.is_finished:
                if game.is_draw:
                    points += 1
                if game.winner == self:
                    points += 3
        return points


class Timeframe(models.Model):
    start = models.DateTimeField(_('from'))
    end = models.DateTimeField(_('to'))

    class Meta:
        ordering = ('start',)
        verbose_name = _('Timeframe')
        verbose_name_plural = _('Timeframes')

    def __unicode__(self):
        return self.start.strftime('%H:%M')

    @property
    def hour(self):
        return self.start.strftime('%H')

    @property
    def minute(self):
        return self.start.strftime('%M')


class Location(models.Model):
    name = models.CharField(_('name'), max_length=20)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __unicode__(self):
        return self.name


class Game(models.Model):
    time = models.ForeignKey(Timeframe)
    location = models.ForeignKey(Location)

    teamA = models.ForeignKey(Team, related_name='games_a')
    teamB = models.ForeignKey(Team, related_name='games_b')

    score_teamA = models.IntegerField(_('Score Team A'), blank=True, null=True)
    score_teamB = models.IntegerField(_('Score Team B'), blank=True, null=True)

    class Meta:
        ordering = ('time', 'location',)
        verbose_name = _('Game')
        verbose_name_plural = _('Games')

    def clean(self):
        from django.core.exceptions import ValidationError

        msg = _(u'%(teamA)s and %(teamB)s dont play in the same tournamentS')
        if self.teamA.tournament != self.teamB.tournament:
            raise ValidationError(msg % {
                'teamA': self.teamA,
                'teamB': self.teamB
            })

        if self.teamA == self.teamB:
            raise ValidationError('A team cannot play agains itself!')

    def __unicode__(self):
        return u"%s - %s" % (self.teamA, self.teamB)

    def goals_shot(self, team):
        if not self.is_finished:
            return 0
        if self.teamA == team:
            return self.score_teamA
        elif self.teamB == team:
            return self.score_teamB
        else:
            return 0

    def goals_received(self, team):
        if not self.is_finished:
            return 0
        if self.teamA == team:
            return self.score_teamB
        elif self.teamB == team:
            return self.score_teamA
        else:
            return 0

    @property
    def tournament(self):
        return self.teamA.tournament

    @property
    def winner(self):
        if self.score_teamA > self.score_teamB:
            return self.teamA
        if self.score_teamA < self.score_teamB:
            return self.teamB
        return None

    @property
    def is_draw(self):
        return self.score_teamA == self.score_teamB

    @property
    def is_finished(self):
        return not self.score_teamA is None and not self.score_teamB is None
