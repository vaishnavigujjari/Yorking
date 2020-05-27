# Generated by Django 3.0.6 on 2020-05-27 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CreateTeam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CreateTeam.User_team')),
            ],
        ),
        migrations.CreateModel(
            name='MatchPerformance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runs', models.IntegerField()),
                ('catches', models.IntegerField()),
                ('wickets', models.IntegerField()),
                ('matchid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CreateTeam.Matches')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CreateTeam.Players')),
            ],
        ),
    ]
