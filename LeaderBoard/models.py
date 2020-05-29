from django.db import models
from CreateTeam.models import Players, Matches, User_team, Choosen_players

class User(models.Model):
    user_id = models.ForeignKey(User_team, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200)

class MatchPerformance(models.Model):
    matchid = models.ForeignKey(Matches, on_delete=models.CASCADE)
    pid = models.ForeignKey(Players, on_delete=models.CASCADE)
    category=models.CharField(max_length=200)
    runs = models.IntegerField()
    catches = models.IntegerField()
    wickets = models.IntegerField()
    class Meta:
        unique_together = (('matchid', 'pid'),)