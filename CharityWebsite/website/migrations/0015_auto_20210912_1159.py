# Generated by Django 3.2.7 on 2021-09-12 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20210911_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('l_goals', models.IntegerField(default=0)),
                ('l_assists', models.IntegerField(default=0)),
                ('l_clean_sheets', models.IntegerField(default=0)),
                ('c_goals', models.IntegerField(default=0)),
                ('c_assists', models.IntegerField(default=0)),
                ('c_clean_sheets', models.IntegerField(default=0)),
                ('f_goals', models.IntegerField(default=0)),
                ('f_assists', models.IntegerField(default=0)),
                ('f_clean_sheets', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='player',
            name='assists',
        ),
        migrations.RemoveField(
            model_name='player',
            name='clean_sheets',
        ),
        migrations.RemoveField(
            model_name='player',
            name='goals',
        ),
        migrations.AlterField(
            model_name='trainingresource',
            name='file',
            field=models.FileField(upload_to='downloadables/'),
        ),
        migrations.AddField(
            model_name='player',
            name='results',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='website.results'),
            preserve_default=False,
        ),
    ]
