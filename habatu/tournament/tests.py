from django.test import TestCase
from datetime import datetime, timedelta

from models import Tournament, Team, Timeframe, Location, Game

class GameTest(TestCase):
    def setUp(self):
        self.time = Timeframe.objects.create(
            start = datetime.now(),
            end = datetime.now() + timedelta(hours=1)
        )
        
        self.location = Location.objects.create(name='testloc')
        
        self.tournament1 = Tournament.objects.create(title='tour1')
        self.tournament2 = Tournament.objects.create(title='tour2')
        
        self.team1 = Team.objects.create(name='team1', tournament=self.tournament1)
        #self.team1.participations.add(self.tournament1)
        #self.team1.save()
        
        self.team2 = Team.objects.create(name='team2', tournament=self.tournament1)
        #self.team2.participations.add(self.tournament1)
        #self.team2.save()
        
        self.team3 = Team.objects.create(name='team3', tournament=self.tournament2)
        #self.team3.participations.add(self.tournament2)
        #self.team3.save()
    
    def test_in_same_tournament(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1, 
            teamB=self.team2,
        )
        
        try:
            game.full_clean()
        except:
            self.fail("Should not raise a (validation) error!")
            
    def test_not_in_same_tournament(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1, 
            teamB=self.team3,
        )
        
        from django.core.exceptions import ValidationError
        self.assertRaises(ValidationError, game.full_clean)
        
    def test_no_winner(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
        )
        
        self.assertEquals(game.winner, None)
        
    def test_has_winner(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=3,
            score_teamB=0,
        )
        
        self.assertEquals(game.winner, self.team1)
        
    def test_unfinishedA(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=3,
        )
        
        self.assertEquals(game.is_finished, False)
        
    def test_unfinishedB(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamB=0,
        )
        
        self.assertEquals(game.is_finished, False)
        
    def test_is_finished_draw1(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=0,
            score_teamB=0,
        )
        
        self.assertEquals(game.is_finished, True)
        self.assertEquals(game.is_draw, True)
        
    def test_is_finished_draw2(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=3,
            score_teamB=3,
        )
        
        self.assertEquals(game.is_finished, True)
        self.assertEquals(game.is_draw, True)

    def test_has_winner1(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=3,
            score_teamB=0,
        )
        
        self.assertEquals(game.is_finished, True)
        self.assertEquals(game.winner, self.team1)
        
    def test_has_winner2(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=0,
            score_teamB=1,
        )
        
        self.assertEquals(game.is_finished, True)
        self.assertEquals(game.winner, self.team2)
        
    def test_points_draw(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=1,
            score_teamB=1,
        )
        
        game.save()
        self.assertEquals(game.is_finished, True)
        self.assertEquals(self.team1.points, 1)
        self.assertEquals(self.team2.points, 1)
        game.delete()

    def test_points_winner1(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=2,
            score_teamB=1,
        )
        
        game.save()
        self.assertEquals(game.is_finished, True)
        self.assertEquals(self.team1.points, 3)
        self.assertEquals(self.team2.points, 0)
        game.delete()
        
    def test_points_winner2(self):
        game = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=1,
            score_teamB=3,
        )
        
        game.save()
        self.assertEquals(game.is_finished, True)
        self.assertEquals(self.team1.points, 0)
        self.assertEquals(self.team2.points, 3)
        game.delete()
        
    def test_points_multiple_games(self):
        game1 = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=3,
            score_teamB=1,
        )
        
        game2 = Game(
            #tournament = self.tournament1,
            time = self.time,
            location = self.location,
            teamA=self.team1,
            teamB=self.team2,
            score_teamA=1,
            score_teamB=1,
        )
        
        game1.save()
        game2.save()
        self.assertEquals(self.team1.points, 4)
        self.assertEquals(self.team2.points, 1)
        game1.delete()
        game2.delete()


