from django.db import models
from django.db import OperationalError

class Players(models.Model):
    pid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    category=models.CharField(max_length=20)
    points=models.IntegerField()
    country=models.CharField(max_length=20)

class Matches(models.Model):
    matchid=models.IntegerField(primary_key=True)
    coun1=models.CharField(max_length=20)
    coun2=models.CharField(max_length=20)
    status=models.CharField(max_length=200)

class User_team(models.Model):
    user_id=models.IntegerField(primary_key=True)
    matchid=models.ForeignKey('Matches',on_delete=models.CASCADE)
    captain=models.IntegerField()
    class Meta:
        unique_together=(('user_id','matchid'),)

class Choosen_players(models.Model):
    user_match=models.ForeignKey('User_team',on_delete=models.CASCADE)
    pid=models.ForeignKey('Players',on_delete=models.CASCADE)
    stars=models.IntegerField(default=0)
    class Meta:
        unique_together=(('user_match','pid'),)