# Generated by Django 3.0.8 on 2020-07-27 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('isDrinking', models.BooleanField(default=False)),
                ('guestEmail', models.EmailField(max_length=254)),
                ('guestIsDrinking', models.BooleanField(default=False)),
            ],
        ),
    ]