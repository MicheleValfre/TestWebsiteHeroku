# Generated by Django 3.2.7 on 2021-10-05 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0033_pitch_pitchdate_pitchtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitch',
            name='group',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='website.team'),
            preserve_default=False,
        ),
    ]
