# Generated by Django 3.2.7 on 2021-09-12 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_auto_20210912_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='results',
        ),
        migrations.AddField(
            model_name='player',
            name='assists',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='clean_sheets',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='goals',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Results',
        ),
    ]
