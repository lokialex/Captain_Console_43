# Generated by Django 3.0.5 on 2020-05-08 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200507_2210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        migrations.AddField(
            model_name='review',
            name='recomend',
            field=models.BooleanField(default=True),
        ),
    ]