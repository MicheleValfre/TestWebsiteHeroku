# Generated by Django 3.2.7 on 2021-10-05 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0035_auto_20211005_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitchtime',
            name='team',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.team'),
        ),
    ]