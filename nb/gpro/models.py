from django.db import models
 
 
class Season(models.Model):
    name = models.IntegerField()
 
    class Meta:
        verbose_name = "Sezon"
        verbose_name_plural = "Sezony"
 
    def __str__(self):
        return f'Sezon {self.name}'
 
 
class Track(models.Model):
    name = models.CharField(max_length=128, verbose_name="Nazwa toru")
 
    class Meta:
        verbose_name = "Tor"
        verbose_name_plural = "Tory"
 
    def __str__(self):
        return f'Tor {self.name}'
 
 
class Race(models.Model):
    track = models.ForeignKey('gpro.Track', on_delete=models.PROTECT, verbose_name="Tor")
    season = models.ForeignKey('gpro.Season', on_delete=models.PROTECT, verbose_name="Sezon")
    identifier = models.IntegerField()
    date = models.DateField(verbose_name="Data wyścigu")
 
    class Meta:
        verbose_name = "Wyścig"
        verbose_name_plural = "Wyścigi"
 
    def __str__(self):
        return f'Wyścig S{self.season.name}R{self.identifier}'