# Generated by Django 3.2.8 on 2021-10-13 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0039_auto_20211005_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=10000)),
                ('photo', models.ImageField(null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='EthosPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=10000)),
                ('photo', models.ImageField(null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='TGAstroPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=10000)),
                ('photo', models.ImageField(null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='WelfarePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=10000)),
                ('photo', models.ImageField(null=True, upload_to='images/')),
            ],
        ),
    ]
