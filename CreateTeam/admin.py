from django.contrib import admin
from .models import country_team, match_user, user_team, choosen_players, match_performance

admin.site.register(country_team)
admin.site.register(match_user)
admin.site.register(user_team)
admin.site.register(choosen_players)
admin.site.register(match_performance)