from django.db import models
from django.db.models.deletion import CASCADE

class Season(models.Model):
    season_number = models.IntegerField()

class Race(models.Model):
    race_number = models.IntegerField()
    track = models.CharField(max_length=30)
    race_date = models.DateField()
    season_number = models.ForeignKey(Season, on_delete=CASCADE)