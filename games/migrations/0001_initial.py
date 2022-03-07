# Generated by Django 3.2.7 on 2022-03-06 21:20

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leagues', '0005_alter_league_status'),
        ('players_profile', '0005_remove_profile_leagues'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('exhibition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches', to='leagues.league')),
                ('first_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches_first_player', to='players_profile.profile')),
                ('second_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches_second_player', to='players_profile.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_player_sets_won', models.SmallIntegerField()),
                ('second_player_sets_won', models.SmallIntegerField()),
                ('first_player_games_won_set_1', models.SmallIntegerField()),
                ('second_player_games_won_set_1', models.SmallIntegerField()),
                ('first_player_games_won_set_2', models.SmallIntegerField()),
                ('second_player_games_won_set_2', models.SmallIntegerField()),
                ('first_player_games_won_set_3', models.SmallIntegerField(blank=True, null=True)),
                ('second_player_games_won_set_3', models.SmallIntegerField(blank=True, null=True)),
                ('game', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='score', to='games.game')),
            ],
        ),
        migrations.AddConstraint(
            model_name='game',
            constraint=models.CheckConstraint(check=models.Q(('first_player', django.db.models.expressions.F('second_player')), _negated=True), name='first_player_and_second_player_can_not_be_equal'),
        ),
    ]