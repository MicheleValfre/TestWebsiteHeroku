# Generated by Django 3.2.7 on 2021-09-14 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0026_agegroupsponsors_sponsors'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AgeGroupSponsors',
            new_name='AgeGroupSponsor',
        ),
        migrations.RenameModel(
            old_name='Sponsors',
            new_name='Sponsor',
        ),
    ]
