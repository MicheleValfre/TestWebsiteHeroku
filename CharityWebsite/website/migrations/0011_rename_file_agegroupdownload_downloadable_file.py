# Generated by Django 3.2.7 on 2021-09-11 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_alter_agegroupdownload_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agegroupdownload',
            old_name='file',
            new_name='downloadable_file',
        ),
    ]
