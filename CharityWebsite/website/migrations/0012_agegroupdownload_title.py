# Generated by Django 3.2.7 on 2021-09-11 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_rename_file_agegroupdownload_downloadable_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='agegroupdownload',
            name='title',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
