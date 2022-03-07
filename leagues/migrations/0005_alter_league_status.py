# Generated by Django 3.2.7 on 2022-03-06 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0004_alter_league_players'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='status',
            field=models.CharField(choices=[('OPEN', 'open'), ('STARTED', 'started'), ('ENDED', 'ended')], default='OPEN', max_length=20),
        ),
    ]
