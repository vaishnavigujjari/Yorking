# Generated by Django 3.0.6 on 2020-05-27 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeaderBoard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stars',
            field=models.IntegerField(default=0),
        ),
    ]
