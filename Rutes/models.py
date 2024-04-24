from django.db import models


# Create your models here.
class Rutes(models.Model):
    RuteId = models.AutoField(primary_key=True)
    RuteName = models.CharField(max_length=50,unique=True)
    # RuteType = models.CharField(max_length=50)
    RuteDescription = models.CharField(max_length=50, null=True, blank=True)
    RuteDistance = models.FloatField()
    RuteTime = models.IntegerField(default=0)
    # RuteDifficulty = models.CharField(max_length=50)
    # RuteElevation = models.IntegerField()
    # RuteImage = models.CharField(max_length=50)
    # RuteLocation = models.CharField(max_length=50)
    RuteRating = models.IntegerField(null=True)
    PuntIniciLat = models.FloatField(null = True)
    PuntIniciLong = models.FloatField(null = True)



class Punts(models.Model):
    PuntId = models.AutoField(primary_key=True)
    PuntName = models.CharField(max_length=50, null=True, blank=True)
    PuntLat = models.FloatField()
    PuntLong = models.FloatField()
    class Meta:
        # Especificar que la combinación de PuntLat y PuntLong debe ser única
        unique_together = ('PuntLat', 'PuntLong')

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