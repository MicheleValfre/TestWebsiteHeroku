from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from django.contrib.staticfiles.storage import staticfiles_storage

#TODO remove this import once all the admin's handles are removed
from django.contrib import admin
from .utils import *

class JoinUsData(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    mail = models.CharField(max_length=100, null=True, blank=True)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True,upload_to="images/")
    description = models.TextField(max_length=2000, null=True)
    user_email = models.EmailField(null=True)
    phone = models.CharField(max_length=50, null=True)
    position = models.IntegerField()
    primary = models.BooleanField()

class Team(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True}
    )
    def __str__(self):
        return self.name




class News(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now=True)


class NewsPhoto(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE
    )
    photo = models.ImageField(null=True, upload_to="images/")

class Results(models.Model):
    #League
    l_goals = models.IntegerField(default=0)
    l_assists = models.IntegerField(default=0)
    l_clean_sheets = models.IntegerField(default=0)
    #Cup
    c_goals = models.IntegerField(default=0)
    c_assists = models.IntegerField(default=0)
    c_clean_sheets = models.IntegerField(default=0)
    #Friendly
    f_goals = models.IntegerField(default=0)
    f_assists = models.IntegerField(default=0)
    f_clean_sheets = models.IntegerField(default=0)

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    dob = models.DateField(null=True, blank=True)
    appears = models.IntegerField(default=0)
    results = models.ForeignKey(
        Results,
        on_delete=models.CASCADE
    )
    FAN = models.IntegerField()

    def __str__(self):
        return self.name

class Event(models.Model):
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    description = models.TextField(max_length=10000)

class Fixture(models.Model):
    group = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    date = models.DateField()
    venue = models.CharField(max_length=1000)
    team = models.CharField(max_length=1000)
    opponent = models.CharField(max_length=1000)
    event = models.CharField(max_length=4000)
    kickoff_time = models.TimeField()
    pom_reds = models.ForeignKey(
        Player,
        related_name="pl_reds",
        on_delete=models.CASCADE
    )
    pom_blacks = models.ForeignKey(
        Player,
        related_name="pl_blcks",
        on_delete=models.CASCADE
    )
    score = models.CharField(max_length=100)
    notes = models.TextField(max_length=5000,null=True)

class MailingListAddress(models.Model):
    list = models.ForeignKey(
        Team,
        on_delete = models.CASCADE
    )
    address = models.CharField(max_length=100)
    child = models.CharField(max_length=200)
    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

class Mail(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    receivers = models.ForeignKey(
        Team,
        on_delete = models.CASCADE
    )
    subject = models.CharField(max_length=100)
    text = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now=True)

class WelcomeMessage(models.Model):
    message = models.TextField(max_length=10000)
    image = models.ImageField(null=True,upload_to="images/")


class AgeGroupWelcomeMessage(models.Model):
    group = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    message = models.TextField(max_length=10000)



class AgeGroupNews(models.Model):
    group = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now=True)

class AgeGroupNewsPhoto(models.Model):
    news = models.ForeignKey(
        AgeGroupNews,
        on_delete=models.CASCADE
    )
    photo = models.ImageField(null=True, upload_to="images/")

class AgeGroupContact(models.Model):
    group = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True,upload_to="images/")
    description = models.TextField(max_length=2000, null=True)
    user_email = models.EmailField(null=True)
    phone = models.CharField(max_length=50, null=True)
    position = models.IntegerField()
    primary = models.BooleanField()

class Download(models.Model):
    downloadable_file = models.FileField(upload_to="downloadables/")
    title = models.CharField(max_length=100)

class AgeGroupDownload(models.Model):
    group = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    downloadable_file = models.FileField(upload_to="downloadables/")
    title = models.CharField(max_length=100)

class Training(models.Model):
    group = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    text = models.TextField(max_length=10000)

class TrainingResource(models.Model):
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="downloadables/")
    description = models.TextField(max_length=1000, null=True)

class Honour(models.Model):
    group = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    honour = models.CharField(max_length=100)
    details = models.CharField(max_length=100, null=True)

class ClubHonour(models.Model):
    honour = models.CharField(max_length=100)
    details = models.CharField(max_length=100, null=True)

class ParentToTeamRelation(models.Model):
    group = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

class Sponsor(models.Model):
    banner = models.ImageField(null=True, upload_to="images/")
    url = models.URLField()

class AgeGroupSponsor(models.Model):
    group = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    banner = models.ImageField(null=True, upload_to="images/")
    url = models.URLField()


class Pitch(models.Model):
    title = models.CharField(max_length=1000)
    group = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )

class PitchDate(models.Model):
    pitch = models.ForeignKey(
        Pitch,
        on_delete=models.CASCADE
    )
    date=models.DateField()

class PitchTime(models.Model):
    pitch_date = models.ForeignKey(
        PitchDate,
        on_delete=models.CASCADE
    )
    time=models.TimeField()
    team=models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )
    ref=models.CharField(max_length=100)
    def __str__(self):
        return str(self.time)

class AboutPage(models.Model):
    text = models.TextField(max_length=10000)
    photo = models.ImageField(null=True, upload_to="images/")


class EthosPage(models.Model):
    text = models.TextField(max_length=10000)
    photo = models.ImageField(null=True, upload_to="images/")



class TGAstroPage(models.Model):
    text = models.TextField(max_length=10000)
    photo = models.ImageField(null=True, upload_to="images/")



class WelfarePage(models.Model):
    text = models.TextField(max_length=10000)
    photo = models.ImageField(null=True, upload_to="images/")




#TODO remove this registration
@admin.register(ParentToTeamRelation)
class PToTAdmin(admin.ModelAdmin):
    pass
