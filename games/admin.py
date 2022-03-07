from django.contrib import admin

# Register your models here.
from games.models import Game, Score

admin.site.register(Game)
admin.site.register(Score)
