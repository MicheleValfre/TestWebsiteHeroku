from django.forms import ModelForm
from django import forms
from django.forms import DateTimeInput
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput

from .models import *
from .utils import *

class JoinUsForm(ModelForm):
    class Meta:
        model = JoinUsData
        fields = '__all__'


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        phone = cleaned_data.get("phone")
        mail = cleaned_data.get("mail")
        if(not name):
            raise forms.ValidationError("you must enter your name!")
        if((not phone) and (not mail)):
            raise forms.ValidationError("you must provide at least a phone number or an e-mail address!")

class WelcomeMessageForm(ModelForm):
    class Meta:
        model=WelcomeMessage
        fields=('message',)
        widgets = {
          'message': forms.Textarea(attrs={'rows':15, 'cols':130}),
        }

class AgeGroupWelcomeMessageForm(ModelForm):
    class Meta:
        model = AgeGroupWelcomeMessage
        fields = ('message',)
        widgets = {
          'message': forms.Textarea(attrs={'rows':15, 'cols':130}),
        }

    def clean(self):
        cleaned_data = super().clean()
        message = cleaned_data.get("message")

class AgeGroupNewsForm(ModelForm):
    class Meta:
        model = AgeGroupNews
        fields = ('title','text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows':15, 'cols':130}),
        }

class ContactForm(ModelForm):
    class Meta:
        model = AgeGroupContact
        fields = ('name','role','photo','description','user_email','phone','position','primary')


class AgeGroupContactForm(ModelForm):
    class Meta:
        model = AgeGroupContact
        fields = ('name','role','photo','description','user_email','phone','position','primary')

class MailingListAddressForm(ModelForm):
    class Meta:
        model = MailingListAddress 
        fields = ('address','child')

class DownloadForm(ModelForm):
    class Meta:
        model = Download
        fields = ('downloadable_file','title')


class AgeGroupDownloadForm(ModelForm):
    class Meta:
        model = AgeGroupDownload
        fields = ('downloadable_file','title')

class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = ('text',)
        widgets = {
          'text': forms.Textarea(attrs={'rows':15, 'cols':130}),
        }

class TrainingResourceForm(ModelForm):
    class Meta:
        model = TrainingResource
        fields = ('file','description')

class HonourForm(ModelForm):
    class Meta:
        model = Honour
        fields = ('honour','details')

class PlayerForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    dob = forms.DateField(label="D.O.B", widget=DatePickerInput())
    appears = forms.IntegerField(label="Appears")
    
    FAN = forms.IntegerField(label="FAN")

class AdminPlayerForm(ModelForm):
    class Meta:
        model=Player
        fields=('team','name','dob','appears','FAN')


class LeagueForm(forms.Form):
    league_goals = forms.IntegerField(label="Goals")
    league_assists = forms.IntegerField(label="Assists")
    league_clean_sheets = forms.IntegerField(label="Clean-Sheets")
     
class CupForm(forms.Form):
    cup_goals = forms.IntegerField(label="Goals")
    cup_assists = forms.IntegerField(label="Assists")
    cup_clean_sheets = forms.IntegerField(label="Clean-Sheets")
    
class FriendlyForm(forms.Form):
    friendly_goals = forms.IntegerField(label="Goals")
    friendly_assists = forms.IntegerField(label="Assists")
    friendly_clean_sheets = forms.IntegerField(label="Clean-Sheets")

class FixtureForm(forms.ModelForm):
    class Meta:
        model=Fixture
        exclude=['group',]
        widgets = {
          'date': DatePickerInput(), 
          'kickoff_time': TimePickerInput()
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model=News
        exclude = []

class EventForm(forms.ModelForm):
    class Meta:
        model=Event
        exclude=['event_type']
        widgets = {
            'date_time': DateTimePickerInput()
        }

class ClubHonourForm(forms.ModelForm):
    class Meta:
        model=ClubHonour
        exclude=[]


def getTeams():
    teams = Team.objects.all()
    choices = [('WJFC','WJFC')]
    for t in teams:
        choices.append((t.id,t.name))
    return choices

class SponsorForm(forms.Form):
    team = forms.ChoiceField(choices=getTeams())
    url = forms.URLField()
    banner = forms.ImageField()


class AgeGroupForm(forms.Form):
    team = forms.ChoiceField(choices=getTeams()[1:])

class MailForm(forms.ModelForm):
    class Meta:
        model = Mail 
        exclude = ['sender','receivers']

class PitchForm(forms.ModelForm):
    class Meta:
        model = Pitch
        exclude = []

class PitchDateForm(forms.ModelForm):
    class Meta:
        model=PitchDate
        exclude=['pitch',]
        widgets = {
          'date': DatePickerInput(), 
        }

class PitchTimeForm(forms.ModelForm):
    class Meta:
        model=PitchTime
        exclude=['pitch_date',]

class TextImageForm(forms.Form):
    image = forms.ImageField(required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':15, 'cols':130}))
