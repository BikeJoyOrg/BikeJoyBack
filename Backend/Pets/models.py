from django.db import models

# Create your models here.
class Mascota(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    img1 = models.IntegerField
    img1l = models.IntegerField
    img2 = models.IntegerField
    img2l = models.IntegerField
    img3 = models.IntegerField
    img3l = models.IntegerField
    bonus = models.CharField(max_length=50)

class MascotaAconseguida(models.Model):
    nomMascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    nicknameUsuari = models.CharField(max_length=50)
    nivell = models.IntegerField(default=1)
    equipada = models.BooleanField(default=False)
