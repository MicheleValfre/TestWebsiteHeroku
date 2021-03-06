# Generated by Django 3.2.7 on 2021-09-14 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0024_rename_events_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubHonour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('honour', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('Tournament', 'Tournament'), ('Foundraising', 'Foundraising')], max_length=20),
        ),
    ]
