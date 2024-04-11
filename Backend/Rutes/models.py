from django.db import models


# Create your models here.
class Rutes(models.Model):
    RuteId = models.AutoField(primary_key=True)
    RuteName = models.CharField(max_length=50)
    # RuteType = models.CharField(max_length=50)
    # RuteDescription = models.CharField(max_length=50)
    RuteDistance = models.FloatField()
    RuteTime = models.IntegerField(default=0)
    # RuteDifficulty = models.CharField(max_length=50)
    # RuteElevation = models.IntegerField()
    # RuteImage = models.CharField(max_length=50)
    # RuteLocation = models.CharField(max_length=50)
    RuteRating = models.IntegerField(null=True)
    PuntIniciLat = models.FloatField()
    PuntIniciLong = models.FloatField()



class Punts(models.Model):
    PuntId = models.AutoField(primary_key=True)
    PuntName = models.CharField(max_length=50, null=True, blank=True,unique=True)
    PuntLat = models.FloatField()
    PuntLong = models.FloatField()


class PuntsIntermedis(models.Model):
    PuntInterId = models.AutoField(primary_key=True)
    PuntOrder = models.IntegerField()
    RuteId = models.ForeignKey(Rutes, on_delete=models.CASCADE)
    PuntId = models.ForeignKey(Punts, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('PuntOrder', 'RuteId', 'PuntId')

class Valoracio(models.Model):
    ValoracioId = models.AutoField(primary_key=True)
    RuteId = models.ForeignKey(Rutes, on_delete=models.CASCADE)
    # UserId = models.IntegerField()
    Valoracio = models.IntegerField()
    # Comentari = models.CharField(max_length=50)
