# Generated by Django 3.2.7 on 2022-03-05 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players_profile', '0005_remove_profile_leagues'),
        ('leagues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='players',
            field=models.ManyToManyField(related_name='leagues', to='players_profile.Profile'),
        ),
    ]
