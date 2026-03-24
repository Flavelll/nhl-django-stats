from django import forms
from django.db import connection

class TeamCompareForm(forms.Form):

    team = forms.MultipleChoiceField(label="Team", required=False)
    season = forms.MultipleChoiceField(label="Season", required=False)
    game_type = forms.MultipleChoiceField(label="Game Type", required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with connection.cursor() as cursor:

            cursor.execute("SELECT DISTINCT team FROM bx ORDER BY team")
            self.fields['team'].choices = [(r[0], r[0]) for r in cursor.fetchall()]

            cursor.execute("SELECT DISTINCT season FROM bx ORDER BY season DESC")
            self.fields['season'].choices = [(r[0], r[0]) for r in cursor.fetchall()]

            cursor.execute("SELECT DISTINCT gametype FROM bx ORDER BY gametype")
            self.fields['game_type'].choices = [(r[0], r[0]) for r in cursor.fetchall()]

