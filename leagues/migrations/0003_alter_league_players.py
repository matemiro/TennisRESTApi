# Generated by Django 3.2.7 on 2022-03-05 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players_profile', '0005_remove_profile_leagues'),
        ('leagues', '0002_league_players'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='players',
            field=models.ManyToManyField(blank=True, null=True, related_name='leagues', to='players_profile.Profile'),
        ),
    ]
