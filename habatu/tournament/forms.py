from django import forms

from models import Game, Team, Timeframe, Location

class GameForm(forms.ModelForm):
    
    teamA = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label='?')
    teamB = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label='?')
    
    time = forms.ModelChoiceField(queryset=Timeframe.objects.all(), empty_label=None)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label=None)
    
    class Meta:
        model = Game
