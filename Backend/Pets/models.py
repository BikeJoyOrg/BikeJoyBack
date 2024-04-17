from django.db import models

# Create your models here.
class Mascota(models.Model):
    name = models.TextField(max_length=50, primary_key=True)
    img1 = models.IntegerField(default=1)
    img1l = models.IntegerField(default=1)
    img2 = models.IntegerField(default=1)
    img2l = models.IntegerField(default=1)
    img3 = models.IntegerField(default=1)
    img3l = models.IntegerField(default=1)
    bonus = models.TextField(max_length=50)

class MascotaAconseguida(models.Model):
    nomMascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    nicknameUsuari = models.CharField(max_length=50)
    nivell = models.IntegerField(default=1)
    equipada = models.BooleanField(default=False)

    class Meta:
        unique_together = (('nomMascota', 'nicknameUsuari'),)