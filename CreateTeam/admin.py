from django.contrib import admin
from .models import Matches, Players, User_team, Choosen_players

admin.site.register(Matches)
admin.site.register(Players)
admin.site.register(User_team)
admin.site.register(Choosen_players)