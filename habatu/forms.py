from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Game, Team, Timeframe, Location

class GameForm(forms.ModelForm):
    teamA = forms.ModelChoiceField(
        queryset=Team.objects.all(), 
        empty_label=None,
    )
    teamB = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        empty_label=None,
    )
    
    time = forms.ModelChoiceField(
        queryset=Timeframe.objects.all(), 
        empty_label=None
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        empty_label=None
    )
    
    class Meta:
        model = Game
        
class GameFormDND(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('time', 'location')
