# Generated by Django 4.1.13 on 2024-04-09 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mascota',
            name='img1',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='mascota',
            name='img1l',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='mascota',
            name='img2',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='mascota',
            name='img2l',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='mascota',
            name='img3',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='mascota',
            name='img3l',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name='mascotaaconseguida',
            unique_together={('nomMascota', 'nicknameUsuari')},
        ),
    ]