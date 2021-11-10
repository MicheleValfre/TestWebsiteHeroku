import os
import calendar
from datetime import datetime, date, time, timedelta
from os.path import exists
from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden, HttpResponseNotFound
from django.template import loader
from django import forms
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.views.static import serve
from django.utils.crypto import get_random_string
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from django.core.mail import send_mail


from .forms import * 
from .models import *
from .utils import *

ERR_RESTRICTED = "This page is restricted!"
ERR_PARENT_OR_COACH = "This page can be viewed by parents or coaches only!"
ERR_COACH = "This page can be viewed by coaches only!"
ERR_PARENT = "This page can be viewed by parents only!"
ERR_ADMIN = "This page can be viewed by administrators only!"

def documents_and_policies(request):
    context = getContext(request)
    return render(request,"website/documents_and_policies.html",context)

def privacy_policy(request):
    context = getContext(request)
    return render(request,"website/privacy_policy.html",context)



def index(request):
    context = getContext(request)
    wmsg = WelcomeMessage.objects.all().first()
    if wmsg != None:
        context['welcome'] = wmsg
    template = loader.get_template('website/index.html')
    return HttpResponse(template.render(context, request))

def dashboard(request):
    context = getContext(request)
    template = loader.get_template('website/dashboard.html')
    return HttpResponse(template.render(context,request))

def signin(request):
    msg = ""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)
        if(user != None):
            return HttpResponseRedirect('/')
        else:
            msg = "Bad username or password"
    else:
        form = AuthenticationForm()
    return render(request, 'website/signin.html', {'form': form, 'msg': msg})

def logoutFunction(request):
    logout(request)
    return HttpResponseRedirect("/")

def events(request):
    template = loader.get_template('website/events.html')
    context = getContext(request) 
    return HttpResponse(template.render(context, request))

def tournaments(request):
    template = loader.get_template('website/tournaments.html')
    context = getContext(request)
    context['tournaments'] = Event.objects.all().filter(event_type="Tournament")
    return HttpResponse(template.render(context, request))

def fundraising(request):
    template = loader.get_template('website/fundraising.html')
    context = getContext(request)
    context['fundraising'] = Event.objects.all().filter(event_type="Foundraising")
    return HttpResponse(template.render(context, request))

def sponsors(request):
    template = loader.get_template('website/sponsors.html')
    context = getContext(request)
    sponsor_objs = Sponsor.objects.all()
    context["sponsors"] = sponsor_objs
    teams = Team.objects.all()
    context["ag_sponsors"] = []
    for t in teams:
        ag_sponsors = AgeGroupSponsor.objects.all().filter(group=t)
        context["ag_sponsors"].append({"name": t.name, "sponsors": ag_sponsors})
    return HttpResponse(template.render(context, request))

def welfare(request):
    template = loader.get_template('website/welfare.html')
    context = getContext(request)
    context['welfare'] = WelfarePage.objects.all().first()
    return HttpResponse(template.render(context, request))

def welfare_policies(request):
    template = loader.get_template('website/welfare_policies.html')
    context = getContext(request)
    return HttpResponse(template.render(context, request))

def teams(request):
    template = loader.get_template('website/teams.html')
    context = getContext(request)
    team_objs = Team.objects.all()
    teams = []
    for t_o in team_objs:
        sponsor_objects = AgeGroupSponsor.objects.all().filter(group=t_o) 
        team = {
            "name":t_o.name,
            "coach": t_o.coach,
            #"info": t_o.infos,
            "sponsors": [] 
        }
        for s_o in sponsor_objects:
            team["sponsors"].append(s_o)
        teams.append(team)
    print("DEBUG_TEAMS")
    print(teams)
    context["teams"] = teams
    return HttpResponse(template.render(context, request))

def general_info(request):
    template = loader.get_template('website/general_info.html')
    context = getContext(request)
    return HttpResponse(template.render(context, request))

def coach_contacts(request):
    template = loader.get_template('website/coach_contacts.html')
    context = getContext(request)
    return HttpResponse(template.render(context, request))

def age_group_sponsor(request):
    template = loader.get_template('website/age_group_sponsor.html')
    context = getContext(request)
    return HttpResponse(template.render(context, request))

def about(request):
    template = loader.get_template('website/about.html')
    context = getContext(request)
    context['about'] = AboutPage.objects.all().first()
    return HttpResponse(template.render(context, request))

def contacts(request):
    template = loader.get_template('website/contacts.html')
    context = getContext(request)
    contacts = Contact.objects.all()
    context['contacts'] = []
    for c in contacts:
        context['contacts'].append({
                                "name" : c.name,
                                "role" : c.role,
                                "photo": c.photo,
                                "description": c.description,
                                "mail" : c.user_email,
                                "phone": c.phone,
                                "position": c.position,
                            })
    context['contacts'] = sorted(context['contacts'],key=lambda c: c["position"])
    return HttpResponse(template.render(context, request))

def ethos(request):
    template = loader.get_template('website/ethos.html')
    context = getContext(request)
    context['ethos'] = EthosPage.objects.all().first()
    return HttpResponse(template.render(context, request))

def news(request):
    template = loader.get_template('website/news.html')
    context = getContext(request)
    news = News.objects.all()
    news = news.order_by('-date')
    context['news'] = []
    for n in news:
        photos = NewsPhoto.objects.all().filter(news=n)
        context['news'].append({
                        'title': n.title,
                        'text': n.text,
                        'date': n.date,
                        'photos': photos
                        })

    return HttpResponse(template.render(context, request))

def astro(request):
    template = loader.get_template('website/astro.html')
    context = getContext(request)
    context['astro'] = TGAstroPage.objects.all().first()
    return HttpResponse(template.render(context, request))

def directions(request):
    template = loader.get_template('website/directions.html')
    context = getContext(request)
    return HttpResponse(template.render(context, request))

def joinus(request):
    msg = ""
    context = getContext(request)
    if request.method == "POST":
        form = JoinUsForm(request.POST)
        if form.is_valid():
            msg = "Form submitted!"
            form.save()
            form = JoinUsForm()
        else:
            msg = "Invalid form!"
    else:
        form = JoinUsForm()
    context['form'] = form
    context['msg'] = msg
    return render(request, 'website/joinus.html',context)

class Calendar(HTMLCalendar):
        def __init__(self, year=None, month=None):
            self.year = year
            self.month = month
            super(Calendar, self).__init__()

        def formatday(self, day, events):
            events_per_day = events.filter(start_time__day=day)
            d = ''
            for event in events_per_day:
                d += f'<li> {event.title} </li>'
            if day != 0:
                return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
            return '<td></td>'

        def formatweek(self, theweek, events):
            week = ''
            for d, weekday in theweek:
                week += self.formatday(d, events)
            return f'<tr> {week} </tr>'

        def formatmonth(self, withyear=True):
            events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

            cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
            cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
            cal += f'{self.formatweekheader()}\n'
            for week in self.monthdays2calendar(self.year, self.month):
                cal += f'{self.formatweek(week, events)}\n'
            return cal



class CalendarView(generic.ListView):
    model = Event
    template_name = 'website/calendar.html'



    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        print(self.request.GET) 
        d = get_date(self.request.GET.get('month', None))
        print("DAY")
        print(d)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        cntx = getContext(self.request)
        print(cntx)
        if 'isAdmin' in cntx:
            context['isAdmin'] = cntx['isAdmin']
        else:
            context['isAdmin'] = False
        
        if 'isParent' in cntx:
            context['isParent'] = cntx['isParent']
        else:
            context['isParent'] = False
        
        if 'isCoach' in cntx:
            context['isCoach'] = cntx['isCoach']
        else:
            context['isCoach'] = False

        context['logged'] = cntx['logged']
        context['name'] = cntx['name']
        return context

def get_date(day):
    if day:
        year, month = (int(x) for x in day.split('-'))
        return date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def editContacts(request):
    context = getContext(request)
    if(context['isAdmin'] == True):
        contacts = Contact.objects.all()
        context['contacts'] = contacts
        template = loader.get_template('website/edit-contacts.html')
        return HttpResponse(template.render(context,request))
    else:
        template = loader.get_template('website/error.html')
        return HttpResponse(template.render({'msg' : ERR_RESTRICTED},request))


#TODO refactoring -> utils.py or similar
def coachToTeam(request):
    try:
        qry = User.objects.all().filter(username=request.user.username)
        coachObj = qry.first()
    except Exception:
        return None

    try:
        qry = Team.objects.all().filter(coach=coachObj)
        team = qry.first()
    except Exception:
        return None

    return team

#TODO refactoring -> utils.py or similar
def parentToTeam(request):
    try:
        qry = User.objects.all().filter(username=request.user.username)
        parentObj = qry.first()
    except Exception:
        return None

    try:
        qry = ParentToTeamRelation.objects.all().filter(parent=parentObj)
        team = qry.first().group
    except Exception:
        return None

    print(team)
    return team


#TODO refactoring -> utils.py or similar
def getContext(request):
    if(request.user.is_authenticated):
        if(request.user):
            user = User.objects.get(username=request.user.username)
        is_coach = False
        is_parent = False
        is_admin = False
        team = "No team"
        welcome_message = "No welcome message" 
        if user.groups.filter(name="Coach").count() == 1:
            is_coach = True
            coachObj = User.objects.get(username=request.user.username) 
            try:
                team = Team.objects.get(coach=coachObj)
            except Exception:
                pass

            try:
                msgs = AgeGroupWelcomeMessage.objects.all().filter(group=team)
                welcome_message = msgs.first() 
                
                welcome_message = welcome_message.message
            except Exception:
                pass
        if user.groups.filter(name="Parent").count() == 1:
            is_parent = True
            try:
                team = parentToTeam(request) 
                msgs = AgeGroupWelcomeMessage.objects.all().filter(group=team)
                welcome_message = msgs.first()
                welcome_message = welcome_message.message
            except Exception:
                pass
        sections = []
        if request.user.is_superuser:
            is_admin = True
            sections = Team.objects.all()
        context = {
            'logged': True, 
            'isAdmin': request.user.is_superuser,
            'isCoach': is_coach,
            'isParent': is_parent,
            'isAdmin': is_admin,
            'name': request.user.username,
            'welcome_message': welcome_message,
            'sections': sections
        }
        if(team == "No team"):
            context["team"] = team
        else:
            context["team"] = team.name
    else:
        context = {
            'logged': False, 
            'isAdmin': False,
            'isCoach': False,
            'isParent': False,
            'isAdmin': False,
            'name': "",
            'welcome_message': "",
            'sections': []
        }
    sponsors = Sponsor.objects.all()
    context['sponsors'] = sponsors
    return context

def coach_edit_welcome(request):
    msg = ""
    context = getContext(request)
    grp = coachToTeam(request)
    if request.method == 'POST':
        form = AgeGroupWelcomeMessageForm(data=request.POST)
        if(form.is_valid()):
            wmsg = form.cleaned_data['message']
            agwm = AgeGroupWelcomeMessage.objects.all().filter(group=grp)
            agwm = agwm.first()
            if agwm == None:
                agwm = AgeGroupWelcomeMessage.objects.create(group=grp, message = wmsg)
            else:
                agwm.message = wmsg
            agwm.save()
            return redirect('/coach/edit_welcome')
    else:
        agwm = AgeGroupWelcomeMessage.objects.all().filter(group=grp)
        if agwm.first() == None:
            form = AgeGroupWelcomeMessageForm()
        else:
            form = AgeGroupWelcomeMessageForm(initial={"message":agwm.first().message})
    context["form"] = form
    return render(request, 'website/coach_edit_msg.html', context)

def view_news(request):
    context = getContext(request)
    if context['isCoach'] == True:
        grp = coachToTeam(request)
    else:
        return HttpResponseForbidden(ERR_COACH) 
    news = AgeGroupNews.objects.all().filter(group=grp)
    news = news.order_by('-date')
    context['news'] = news
    return render(request, 'website/view_news.html',context)
    

def coach_edit_news(request):
    context = getContext(request)
    grp = coachToTeam(request)
    if request.method == 'POST':
        form = AgeGroupNewsForm(data=request.POST)
        if(form.is_valid()):
            text = form.cleaned_data["text"]
            title = form.cleaned_data["title"]
            agnws = AgeGroupNews(group=grp,title=title,text=text)
            agnws.save();
            return redirect('/coach/view_news') 
    form = AgeGroupNewsForm()
    context["form"] = form
    return render(request, 'website/coach_edit_news.html',context)

def coach_delete_news(request, n_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    news = AgeGroupNews.objects.all().filter(group=grp, id=n_id)
    to_delete = news.first()
    if to_delete == None:
        return HttpResponseNotFound("The requested news doesn't exist!")
    news.delete()
    return redirect('/coach/view_news')

def coach_edit_contacts(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    if(request.method == 'GET'):
        contacts = AgeGroupContact.objects.all().filter(group=grp)
        context['contacts'] = contacts
        return render(request,'website/coach_edit_contacts.html',context)

def coach_add_contact(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    if request.method == 'POST':
        form = AgeGroupContactForm(request.POST, request.FILES)
        if form.is_valid():
            n_cntct = AgeGroupContact(
                group=grp,
                name=form.cleaned_data['name'],
                role=form.cleaned_data['role'],
                photo=form.cleaned_data['photo'],
                description=form.cleaned_data['description'],
                user_email=form.cleaned_data['user_email'],
                phone=form.cleaned_data['phone'],
                position=form.cleaned_data['position'],
                primary=form.cleaned_data['primary']
            )
            n_cntct.save()
            return redirect('/coach/edit_team_contacts')
    form = AgeGroupContactForm()
    context['form'] = form
    return render(request, 'website/coach_add_contact.html',context)

def coach_delete_contact(request,c_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    contacts = AgeGroupContact.objects.all().filter(group=grp, id=c_id)
    to_delete = contacts.first()
    if to_delete == None:
        return HttpResponseNotFound("The requested contact doesn't exist!")
    print(to_delete.photo)
    if to_delete.photo:
        fpath = to_delete.photo.path
        os.remove(fpath)
    contacts.delete()
    return redirect('/coach/edit_team_contacts')

def coach_edit_contact(request,c_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    contacts = AgeGroupContact.objects.all().filter(group=grp, id=c_id)
    c = contacts.first()
    if c == None:
        return HttpResponseNotFound("The requested contact doesn't exist!")
    if request.method == 'POST':
        form = ContactForm(request.POST,request.FILES)
        if form.is_valid():
            c = AgeGroupContact(
                group=grp,
                name=form.cleaned_data['name'],
                role=form.cleaned_data['role'],
                description=form.cleaned_data['description'],
                user_email=form.cleaned_data['user_email'],
                phone=form.cleaned_data['phone'],
                position=form.cleaned_data['position'],
                primary=form.cleaned_data['primary']
            )
            ph = form.cleaned_data['photo']
            if ph != None:
                c.photo = ph
            c.save()
            return redirect('/coach/edit_team_contacts')

    else:
        context['form'] = ContactForm(initial={
            'name': c.name,
            'role': c.role,
            'description': c.description,
            'user_email': c.user_email,
            'phone': c.phone,
            'position': c.position,
            'primary': c.primary
        })
    return render(request,"website/coach_edit_contact.html",context) 


def coach_edit_mail_list(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    mlist = MailingListAddress.objects.all().filter(list=grp)
    context['mlist'] = mlist
    return render(request,'website/coach_edit_mail_list.html',context)

def coach_add_mail(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    if request.method == 'POST':
        form = MailingListAddressForm(request.POST)
        if form.is_valid():
            naddrs = form.cleaned_data['address']
            nchld = form.cleaned_data['child']
            nmail = MailingListAddress(list=grp,address=naddrs,child=nchld)
            nmail.save()
            return redirect('/coach/mail_list')
    form = MailingListAddressForm()
    context['form'] = form
    return render(request,'website/coach_add_mail.html',context)

def coach_delete_mail(request, m_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    mailaddr = MailingListAddress.objects.all().filter(list=grp, id=m_id)
    to_delete = mailaddr.first()
    if to_delete == None:
        return HttpResponseNotFound("The requested address doesn't exist!")
    mailaddr.delete()
    return redirect('/coach/mail_list')

def coach_team_downloads(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    downloads = AgeGroupDownload.objects.all().filter(group=grp)
    context['downloads'] = downloads
    return render(request,"website/coach_team_downloads.html",context)

def coach_add_download(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    if request.method == 'POST':
        print('POST')
        print(request.FILES)
        form = AgeGroupDownloadForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            #TODO handle file uploads        
            print("OK")
            f = form.cleaned_data['downloadable_file']
            old_name = f.name
            name_ok = False
            while not name_ok:
                ext = get_extension(f.name)
                new_name = get_random_string() + ext 
                fname = os.path.join('downloadables/',new_name)
                print('DIOBESTIA')
                print(fname)
                npath = os.path.join(settings.MEDIA_ROOT, fname)
                print('PATH')
                print(npath)
                name_ok = not exists(npath)
                f.name = new_name
            t = form.cleaned_data['title']
            agd = AgeGroupDownload(group=grp,downloadable_file=f,title=t)
            agd.save()
            return redirect("/coach/team_downloads")
    form = AgeGroupDownloadForm()
    context['form'] = form
    return render(request,"website/coach_add_download.html",context)

def coach_delete_download(request,d_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    agd = AgeGroupDownload.objects.all().filter(group=grp, id=d_id)
    if(agd.first() == None):
        return HttpResponseNotFound("The requested file doesn't exist!")
    path = agd.first().downloadable_file.path
    os.remove(path)
    agd.delete()
    return redirect("/coach/team_downloads")

#TODO move to utils
def get_extension(fname):
    ext = fname.rsplit('.',1)
    print(ext)
    return '.' + ext[1]

def coach_view_training(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    training = Training.objects.all().filter(group=grp)
    context['training_info'] = training.first()
    trng = Training.objects.all().filter(group=grp).first()
    if trng == None:
        return HttpResponseNotFound('Something went wrong! No Training object associated with this user group!')
    context['resources'] = TrainingResource.objects.all().filter(training=trng)
    print(context['resources'])
    return render(request,'website/coach_view_training.html',context)

def coach_edit_training(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    current = Training.objects.all().filter(group=grp).first()
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            txt = form.cleaned_data['text']
            print(txt)
            if current == None:
                current = Training.objects.create(group=grp, text=txt)
            else:
                current.text = txt

            current.save()
            return redirect('/coach/training')
    cet = Training.objects.all().filter(group=grp)
    if cet.first() == None:
        form = TrainingForm()
    else:
        form = TrainingForm(initial={"text":cet.first().text})
    context['form'] = form
    
    return render(request,'website/coach_edit_training.html',context)

def coach_add_training_resource(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    trng = Training.objects.all().filter(group=grp).first()
    if trng == None:#should be impossible
        return HttpResponseNotFound('Something went wrong! No Training object associated with this user group!')
    if request.method == 'POST':
        res = TrainingResourceForm(request.POST,request.FILES)
        print('POST')
        print(request.FILES)
        form = TrainingResourceForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            print("OK")
            f = form.cleaned_data['file']
            d = form.cleaned_data['description']
            old_name = f.name
            name_ok = False
            while not name_ok:
                ext = get_extension(f.name)
                new_name = get_random_string() + ext 
                fname = os.path.join('downloadables/',new_name)
                print('DIOBESTIA')
                print(fname)
                npath = os.path.join(settings.MEDIA_ROOT, fname)
                print('PATH')
                print(npath)
                name_ok = not exists(npath)
                f.name = new_name
            tr = TrainingResource(training=trng,file=f,description=d)
            tr.save()
            return redirect("/coach/training")
    form = TrainingResourceForm()
    context['form'] = form
    return render(request,"website/coach_add_training_resource.html",context)


def coach_remove_training_resource(request,r_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    trng = Training.objects.all().filter(group=grp).first()
    trng_resource = TrainingResource.objects.all().filter(training=trng,id=r_id)
    to_delete = trng_resource.first()
    if to_delete == None:
        return HttpResponseNotFound("The requested resource doesn't exist!")
    trng_resource.delete()
    return redirect('/coach/training')

def coach_view_honours(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    hnrs = Honour.objects.all().filter(group=grp)
    context['honours'] = hnrs
    return render(request,'website/coach_view_honours.html',context)

def coach_delete_honour(request,h_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    hnr = Honour.objects.all().filter(group=grp,id=h_id)
    to_delete = hnr.first()
    if to_delete == None:
        return HttpResponseNotFound("The requested honour doesn't exist!")
    hnr.delete()
    return redirect('/coach/honours')


def coach_add_honour(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    if request.method == 'POST':
        form = HonourForm(request.POST)
        if form.is_valid():
            h = form.cleaned_data['honour']
            d = form.cleaned_data['details']
            hnr = Honour(group=grp,honour=h,details=d)
            hnr.save()
            return redirect('/coach/honours')
    context['form'] = HonourForm()
    return render(request,'website/coach_add_honour.html',context)

def coach_view_players(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    players = Player.objects.all().filter(team=grp)
    context['players'] = players
    return render(request,"website/coach_view_players.html",context)

def coach_add_player(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        l_form = LeagueForm(request.POST)
        c_form = CupForm(request.POST)
        f_form = FriendlyForm(request.POST)
        print(form)
        if form.is_valid() and l_form.is_valid() and c_form.is_valid() and f_form.is_valid():
            pr = Results(
                l_goals = l_form.cleaned_data['league_goals'],
                l_assists = l_form.cleaned_data['league_assists'],
                l_clean_sheets = l_form.cleaned_data['league_clean_sheets'],
                c_goals = c_form.cleaned_data['cup_goals'],
                c_assists = c_form.cleaned_data['cup_assists'],
                c_clean_sheets = c_form.cleaned_data['cup_clean_sheets'],
                f_goals = f_form.cleaned_data['friendly_goals'],
                f_assists = f_form.cleaned_data['friendly_assists'],
                f_clean_sheets = f_form.cleaned_data['friendly_clean_sheets']
            )
            pr.save()
            p = Player(
                name=form.cleaned_data['name'],
                team=grp,
                dob=form.cleaned_data['dob'],
                appears=form.cleaned_data['appears'],
                results = pr,
                FAN = form.cleaned_data['FAN']
            )
            p.save()
            return redirect('/coach/players')
    context['form'] = PlayerForm()
    context['l_form'] = LeagueForm()
    context['c_form'] = CupForm()
    context['f_form'] = FriendlyForm()
    return render(request,"website/coach_add_player.html",context)


def coach_delete_player(request,p_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    p = Player.objects.all().filter(team=grp,id=p_id)
    if p.first() == None:
        return HttpResponseNotFound("Player not found!")
    p.first().results.delete()
    p.delete()
    return redirect('/coach/players')

def coach_view_fixtures(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    context['fixtures'] = Fixture.objects.all().filter(group=grp)
    return render(request,'website/coach_view_fixtures.html',context)

def coach_add_fixture(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    if request.method == 'POST':
        form = FixtureForm(request.POST)
        print(form)
        if form.is_valid():
            f = Fixture(
                group=grp,
                venue=form.cleaned_data['venue'],
                team=form.cleaned_data['team'],
                opponent=form.cleaned_data['opponent'],
                event=form.cleaned_data['event'],
                pom_reds=form.cleaned_data['pom_reds'],
                pom_blacks= form.cleaned_data['pom_blacks'],
                score=form.cleaned_data['score'],
                notes=form.cleaned_data['notes'],
                date=form.cleaned_data['date'],
                kickoff_time=form.cleaned_data['kickoff_time']
            )
            f.save()
            return redirect('/coach/fixtures')
    context['form'] = FixtureForm()
    return render(request,"website/coach_add_fixture.html",context)

def details_fixture(request, f_id):
    context = getContext(request)
    if context['isCoach']:
        grp = coachToTeam(request)
        details_template = 'website/coach_fixture_details.html'
    elif context['isParent']:
        grp = parentToTeam(request)
        details_template = 'website/parent_fixture_details.html'
    else:
        return HttpResponseForbidden(ERR_PARENT_OR_COACH)
    f = Fixture.objects.all().filter(group=grp, id=f_id)
    if f.first() == None:
        HttpResponseNotFound("The requested fixture doesn't exist!")
    context['fixture'] = f.first()
    return render(request,details_template,context)

def coach_delete_fixture(request,f_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    fix = Fixture.objects.all().filter(group=grp, id=f_id)
    if fix.first() == None:
        return HttpResponseNotFound("The requested fixture doesn't exist!")
    fix.delete()
    return redirect('/coach/fixtures')


def coach_view_pitches(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    context['pitches'] = Pitch.objects.all()
    
    return render(request,'website/coach_view_pitches.html',context)

def coach_view_pitch(request,p_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    p = Pitch.objects.all().filter(id=p_id).first()
    if p == None:
        return HttpResponseNotFound("Pitch not found")
    context["pitch"] = {}
    context["pitch"]["id"] = p.id
    context["pitch"]["title"] = p.title
    dates = PitchDate.objects.all().filter(pitch=p)
    context["pitch"]["dates"] = dates
    context["pitch"]["times"] = []
    for d in dates:
        tms = PitchTime.objects.all().filter(pitch_date=d)
        for t in tms:
            context["pitch"]["times"].append(t)

    print(context["team"])
    return render(request,'website/coach_view_pitch.html',context)

def coach_book_pitch(request,p_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    pitch = PitchTime.objects.all().filter(id=p_id).first()
    if pitch == None:
        return HttpResponseNotFound("Pitch not found")
    pitch.team = grp
    pitch.save()
    pitch_id = pitch.pitch_date.pitch.id
    return redirect('/coach/view_pitch/' + str(pitch_id))

def coach_unbook_pitch(request,p_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    pitch = PitchTime.objects.all().filter(id=p_id).first()
    if pitch == None:
        return HttpResponseNotFound("Pitch not found")
    pitch.team = None
    pitch.save()
    pitch_id = pitch.pitch_date.pitch.id

    return redirect('/coach/view_pitch/' + str(pitch_id))


def coach_add_pitch(request):
    return HttpResponse("OK")

def coach_delete_pitch(request,p_id):
    return HttpResponse("OK")

#PARENT
def parent_fixture_teams(request,f_id):
    return HttpResponse("TODO");

def parent_view_news(request):
    context = getContext(request)
    if context['isParent'] == True:
        grp = parentToTeam(request)
    else:
        return HttpResponseForbidden(ERR_PARENT) 
    news = AgeGroupNews.objects.all().filter(group=grp)
    news = news.order_by('-date')
    context['news'] = news
    return render(request, 'website/parent_view_news.html',context)


def parent_view_training(request):
    context = getContext(request)
    if context['isParent'] == True:
        grp = parentToTeam(request)
    else:
        return HttpResponseForbidden(ERR_PARENT) 
    training = Training.objects.all().filter(group=grp)
    context['training_info'] = training.first()
    trng = Training.objects.all().filter(group=grp).first()
    if trng == None:
        return HttpResponseNotFound('Something went wrong! No Training object associated with this user group!')
    context['resources'] = TrainingResource.objects.all().filter(training=trng)
    return render(request,'website/parent_view_training.html',context)


def parent_view_contacts(request):
    context = getContext(request)
    if not context['isParent']:
        return HttpResponseForbidden(ERR_PARENT)
    grp = parentToTeam(request)
    contacts = AgeGroupContact.objects.all().filter(group=grp)
    context['contacts'] = contacts
    return render(request,'website/parent_view_contacts.html',context)


def parent_view_downloads(request):
    context = getContext(request)
    if not context['isParent']:
        return HttpResponseForbidden(ERR_PARENT)
    grp = parentToTeam(request)
    context['club_downloads'] = Download.objects.all()
    context['ag_downloads'] = AgeGroupDownload.objects.all().filter(group=grp)
    return render(request,'website/parent_view_downloads.html',context)


def parent_view_fixtures(request):
    context = getContext(request)
    if not context['isParent']:
        return HttpResponseForbidden(ERR_PARENT)
    grp = parentToTeam(request)
    context['fixtures'] = Fixture.objects.all().filter(group=grp)
    return render(request,'website/parent_view_fixtures.html',context)


def parent_view_players(request):
    context = getContext(request)
    if not context['isParent']:
        return HttpResponseForbidden(ERR_PARENT)
    grp = parentToTeam(request)
    players = Player.objects.all().filter(team=grp)
    context['players'] = players
    return render(request,"website/parent_view_players.html",context)

def parent_view_statistics(request):
    return HttpResponse("OK")

def getAssociatedMails(parent):
    return MailingListAddress.objects.all().filter(parent=parent)

def parent_mail_list_unsubscribe(request,m_id):
    context = getContext(request)
    if not context['isParent']:
        return HttpResponseForbidden(ERR_PARENT)
    m = MailingListAddress.objects.all().filter(id=m_id)
    if m.first() == None:
        return HttpResponseNotFound("The required mail doesn't exist")
    m.delete()
    return redirect('/parent/emails')

def parent_mail_list_subscribe(request):
    context = getContext(request)
    if not context['isParent']:
        return HttpResponseForbidden(ERR_PARENT)
    grp = parentToTeam(request)
    context['other_mails'] = getAssociatedMails(request.user)
    if request.method == 'POST':
        form = MailingListAddressForm(request.POST)
        if form.is_valid():
            naddrs = form.cleaned_data['address']
            nchld = form.cleaned_data['child']
            nmail = MailingListAddress(list=grp,address=naddrs,child=nchld,parent=request.user)
            nmail.save()
            return redirect('/parent/emails')
    form = MailingListAddressForm()
    context['form'] = form
    return render(request,'website/parent_mail_list_subscribe.html',context)

def parent_view_honours(request):
    context = getContext(request)
    if not context['isParent']:
        return HttpResponseForbidden(ERR_PARENT)
    grp = parentToTeam(request)
    hnrs = Honour.objects.all().filter(group=grp)
    context['honours'] = hnrs
    context['club_honours'] = ClubHonour.objects.all().filter()
    return render(request,'website/parent_view_honours.html',context)


def admin_edit_info(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    return render(request,"website/admin_edit_info.html",context)

def admin_edit_ethos(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    ethos = EthosPage.objects.all().first()
    if ethos == None:
        ethos = ""
    if request.method == 'POST':
        form = TextImageForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            if ethos == "":
                ethos = EthosPage()
            ethos.text=form.cleaned_data['text']
            print(form.cleaned_data['image'] == None)
            if form.cleaned_data['image'] != None:
                ethos.photo = form.cleaned_data['image']
            ethos.save()
            return redirect('/superuser/edit_info')
    if ethos != "":
        context['form'] = TextImageForm(initial={"text":ethos.text})
    else:
        context['form'] = TextImageForm()
    context['ethos'] = ethos
    return render(request,"website/admin_edit_ethos.html",context)


def admin_edit_3g_astro(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    astro = TGAstroPage.objects.all().first()
    if astro == None:
        astro = ""
    if request.method == 'POST':
        form = TextImageForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            if astro == "":
                astro = TGAstroPage()
            astro.text=form.cleaned_data['text']
            if form.cleaned_data['image'] != None:
                astro.photo = form.cleaned_data['image']
            astro.save()
            return redirect('/superuser/edit_info')
    if astro != "":
        context['form'] = TextImageForm(initial={"text":astro.text})
    else:
        context['form'] = TextImageForm()
    context['astro'] = astro
    return render(request,"website/admin_edit_3g_astro.html",context)

def admin_edit_about(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    about = AboutPage.objects.all().first()
    if about == None:
        about = ""
    if request.method == 'POST':
        form = TextImageForm(request.POST,request.FILES)
        if form.is_valid():
            if about == "":
                about = AboutPage()
            about.text=form.cleaned_data['text']
            if form.cleaned_data['image'] != None:
                about.photo = form.cleaned_data['image']
            about.save()
            return redirect('/superuser/edit_info')
    if about != "":
        context['form'] = TextImageForm(initial={"text":about.text})
    else:
        context['form'] = TextImageForm()
    context['about'] = about
    return render(request,"website/admin_edit_about.html",context)



def admin_edit_welfare(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    welfare = WelfarePage.objects.all().first()
    if welfare == None:
        welfare = ""
    if request.method == 'POST':
        form = TextImageForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            if welfare == "":
                welfare = WelfarePage()
            welfare.text=form.cleaned_data['text']
            if form.cleaned_data['image'] != None:
                welfare.photo = form.cleaned_data['image']
            welfare.save()
            return redirect('/superuser/edit_info')
    if welfare != "":
        context['form'] = TextImageForm(initial={"text":welfare.text})
    else:
        context['form'] = TextImageForm()
    context['welfare'] = welfare
    return render(request,"website/admin_edit_welfare.html",context)


def admin_edit_welcome(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    welcome_msg = WelcomeMessage.objects.all().first()
    if welcome_msg == None:
        welcome_msg = ""
    if request.method == 'POST':
        form = TextImageForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            if welcome_msg == "":
                welcome_msg = WelcomeMessage()
            welcome_msg.message=form.cleaned_data['text']
            if form.cleaned_data['image'] != None:
                welcome_msg.image = form.cleaned_data['image']
            welcome_msg.save()
            return redirect('/superuser/welcome')
    if welcome_msg != "":
        context['form'] = TextImageForm(initial={"text":welcome_msg.message})
    else:
        context['form'] = TextImageForm()
    context['welcome_msg'] = welcome_msg 
    return render(request,"website/admin_edit_msg.html",context)


def admin_edit_news(request):
    template = loader.get_template('website/admin_edit_news.html')
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    news = News.objects.all()
    news = news.order_by('-date')
    news_fin = []
    for n in news:
        n_phs = NewsPhoto.objects.all().filter(news=n)
        tmp = {
            'id': n.id,
            'title': n.title,
            'date':n.date,
            'text':n.text,
            'photos': []
        }
        for n_ph in n_phs:
            tmp['photos'].append(n_ph)
        news_fin.append(tmp)
    context['news'] = news_fin 
    print(news_fin)
    return HttpResponse(template.render(context, request))

def admin_add_news_img(request, n_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    current_n = News.objects.all().filter(id=n_id).first()
    if current_n == None:
        return HttpResponseNotFound("Requested news entry doesn't exist")
    if request.method == "POST":
        images = request.FILES.getlist('images')
        for image in images:
            np = NewsPhoto(news=current_n,photo=image)
            np.save()
    context['images']= NewsPhoto.objects.all().filter(news=current_n)
    context['n_id'] = n_id
    return render(request, 'website/add_news_img.html', context)

def admin_del_news_img(request,i_id,n_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponse(ERR_ADMIN)
    img = NewsPhoto.objects.all().filter(id=i_id).first()
    if img == None:
        return HttpResponse("Image not found")
    img.delete()
    return redirect('/superuser/news_img/' + str(n_id))

def admin_create_news(request):
    context = getContext(request)
    if not request.user.is_superuser:
        return HttpResponse(ERR_ADMIN)
    if request.method == 'POST':
        form = NewsForm(data=request.POST)
        if(form.is_valid()):
            text = form.cleaned_data["text"]
            title = form.cleaned_data["title"]
            agnws = News(title=title,text=text)
            agnws.save();
            return redirect('/superuser/news') 
    form = NewsForm()
    context["form"] = form
    return render(request, 'website/admin_create_news.html',context)

def admin_delete_news(request, n_id):
    context = getContext(request)
    if not request.user.is_superuser:
        return HttpResponseForbidden(ERR_ADMIN)
    news = News.objects.all().filter(id=n_id)
    to_delete = news.first()
    if to_delete == None:
        return HttpResponseNotFound("The requested news doesn't exist!")
    news.delete()
    return redirect('/superuser/news')

def admin_edit_contacts(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    contacts = Contact.objects.all()
    context['contacts'] = contacts
    print(contacts)
    return render(request,'website/admin_edit_contacts.html',context)

def admin_edit_contact(request, c_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)

    contact = Contact.objects.all().filter(id=c_id).first()
    if contact == None:
        return HttpResponseNotFound("Contact not found")
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            contact.name=form.cleaned_data['name'],
            contact.role=form.cleaned_data['role'],
            contact.description=form.cleaned_data['description'],
            contact.user_email=form.cleaned_data['user_email'],
            contact.phone=form.cleaned_data['phone'],
            contact.position=form.cleaned_data['position'],
            contact.primary=form.cleaned_data['primary']
            contact.save()
            return redirect('/superuser/contacts')
    form = ContactForm(initial={
        "name": contact.name,
        "role": contact.role,
        "description": contact.description,
        "user_email": contact.user_email,
        "phone": contact.phone,
        "position": contact.position,
        "primary": contact.primary
    })
    del form.fields['photo']
    context['form'] = form
    return render(request, 'website/admin_add_contact.html',context)

def admin_add_contact(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            n_cntct = Contact(
                name=form.cleaned_data['name'],
                role=form.cleaned_data['role'],
                photo=form.cleaned_data['photo'],
                description=form.cleaned_data['description'],
                user_email=form.cleaned_data['user_email'],
                phone=form.cleaned_data['phone'],
                position=form.cleaned_data['position'],
                primary=form.cleaned_data['primary']
            )
            n_cntct.save()
            return redirect('/superuser/contacts')
    form = ContactForm()
    context['form'] = form
    return render(request, 'website/admin_add_contact.html',context)

def admin_delete_contact(request, c_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    contacts = Contact.objects.all().filter(id=c_id)
    to_delete = contacts.first()
    if to_delete == None:
        return HttpResponseNotFound("The requested contact doesn't exist!")
    fpath = to_delete.photo.path
    os.remove(fpath)
    contacts.delete()
    return redirect('/superuser/contacts')




def admin_edit_downloads(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    downloads = Download.objects.all()
    context['downloads'] = downloads
    return render(request,"website/admin_edit_downloads.html",context)

def admin_add_download(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    if request.method == 'POST':
        form = DownloadForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['downloadable_file']
            old_name = f.name
            name_ok = False
            while not name_ok:
                ext = get_extension(f.name)
                new_name = get_random_string() + ext 
                fname = os.path.join('downloadables/',new_name)
                npath = os.path.join(settings.MEDIA_ROOT, fname)
                name_ok = not exists(npath)
                f.name = new_name
            t = form.cleaned_data['title']
            d = Download(downloadable_file=f,title=t)
            d.save()
            return redirect("/superuser/downloads")
    form = DownloadForm()
    context['form'] = form
    return render(request,"website/admin_add_download.html",context)

def admin_delete_download(request,d_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    agd = Download.objects.all()
    if(agd.first() == None):
        return HttpResponseNotFound("The requested file doesn't exist!")
    path = agd.first().downloadable_file.path
    os.remove(path)
    agd.delete()
    return redirect("/superuser/downloads")


def admin_edit_players(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    players = Player.objects.all()
    context['players'] = players
    return render(request,"website/admin_view_players.html",context)

def admin_add_player(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    if request.method == 'POST':
        form = AdminPlayerForm(request.POST)
        l_form = LeagueForm(request.POST)
        c_form = CupForm(request.POST)
        f_form = FriendlyForm(request.POST)
        if form.is_valid() and l_form.is_valid() and c_form.is_valid() and f_form.is_valid():
            pr = Results(
                l_goals = l_form.cleaned_data['league_goals'],
                l_assists = l_form.cleaned_data['league_assists'],
                l_clean_sheets = l_form.cleaned_data['league_clean_sheets'],
                c_goals = c_form.cleaned_data['cup_goals'],
                c_assists = c_form.cleaned_data['cup_assists'],
                c_clean_sheets = c_form.cleaned_data['cup_clean_sheets'],
                f_goals = f_form.cleaned_data['friendly_goals'],
                f_assists = f_form.cleaned_data['friendly_assists'],
                f_clean_sheets = f_form.cleaned_data['friendly_clean_sheets']
            )
            pr.save()
            p = Player(
                name=form.cleaned_data['name'],
                team=form.cleaned_data['team'],
                dob=form.cleaned_data['dob'],
                appears=form.cleaned_data['appears'],
                results = pr,
                FAN = form.cleaned_data['FAN']
            )
            p.save()
            return redirect('/superuser/players')
    context['form'] = AdminPlayerForm()
    context['l_form'] = LeagueForm()
    context['c_form'] = CupForm()
    context['f_form'] = FriendlyForm()
    return render(request,"website/admin_add_player.html",context)


def admin_delete_player(request,p_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    p = Player.objects.all().filter(id=p_id)
    if p.first() == None:
        return HttpResponseNotFound("Player not found!")
    p.first().results.delete()
    p.delete()
    return redirect('/superuser/players')



def admin_edit_events(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    context['tournaments'] = Event.objects.all().filter(event_type=getType("T"))
    context['foundraising'] = Event.objects.all().filter(event_type=getType("F"))
    return render(request,'website/admin_edit_event.html',context)

def admin_add_tournament(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            evnt = Event(
                event_type=getType("T"),
                title=form.cleaned_data['title'],
                start_time=form.cleaned_data['start_time'],
                description=form.cleaned_data['description']
            )
            evnt.save()
            return redirect('/superuser/events')
    form = EventForm()
    context['form'] = form
    return render(request,'website/admin_add_event.html',context)

def admin_add_foundraising(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            evnt = Event(
                event_type=getType("F"),
                title=form.cleaned_data['title'],
                start_time=form.cleaned_data['start_time'],
                description=form.cleaned_data['description']
            )
            evnt.save()
            return redirect('/superuser/events')
    form = EventForm()
    context['form'] = form
    return render(request,'website/admin_add_event.html',context)


def admin_view_emails(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    mlist = MailingListAddress.objects.all()
    context['mlist'] = mlist
    return render(request,'website/admin_view_emails.html',context)

def admin_send_mail(request,m_id):
    return HttpResponse("TODO")

def admin_edit_pitches(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    context['pitches'] = Pitch.objects.all()
    return render(request,"website/admin_edit_pitches.html",context)

def admin_pitch_add_time(request,p_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    pd = PitchDate.objects.all().filter(id=p_id)
    if pd.first() == None:
        return HttpResponseNotFound("Pitch not found")
    if request.method == 'POST':
        form = PitchTimeForm(request.POST)
        if form.is_valid():
            time = form.cleaned_data['time']
            t = form.cleaned_data['team']
            r = form.cleaned_data['ref']
            pt = PitchTime(time=time,pitch_date=pd.first(),team=t,ref=r)
            pt.save()
            return redirect('/superuser/pitches/edit/' + str(pd.first().pitch.id))
    context['form'] = PitchTimeForm()
    return render(request,"website/admin_pitches_set_time.html",context)

def admin_pitch_delete_date(request,p_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    pd = PitchDate.objects.all().filter(id=p_id)
    if pd.first() == None:
        return HttpResponseNotFound("Pitch not found")
    pid = pd.first().pitch.id
    pd.delete()
    return redirect('/superuser/pitches/edit/'+str(pid))

def admin_pitch_add_date(request,p_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    pitch = Pitch.objects.all().filter(id=p_id)
    pitch = pitch.first()
    if pitch == None:
        return HttpResponseNotFound("Pitch not found")
    if request.method == 'POST':
        form = PitchDateForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            date = form.cleaned_data["date"]
            pd = PitchDate(pitch=pitch,date=date)
            pd.save()
            return redirect('/superuser/pitches/edit/' + str(pitch.id))
    
    context['form'] = PitchDateForm()
    return render(request,'website/admin_edit_pitch_date.html',context)


def admin_edit_pitch(request,p_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    pitches = Pitch.objects.all().filter(id=p_id)
    if pitches.first() == None:
        return HttpResponseNotFound("Pitch not found!")
    p = pitches.first()
    context["pitch"] = {}
    context["pitch"]["id"] = p.id
    context["pitch"]["title"] = p.title
    dates = PitchDate.objects.all().filter(pitch=p)
    context["pitch"]["dates"] = dates
    context["pitch"]["times"] = []
    for d in dates:
        tms = PitchTime.objects.all().filter(pitch_date=d)
        for t in tms:
            context["pitch"]["times"].append(t)
    return render(request,"website/admin_edit_pitch.html",context)

def admin_new_pitch(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)

    if request.method == "POST":
        form = PitchForm(request.POST)
        if form.is_valid():
            np = Pitch(title=form.cleaned_data['title'],group=form.cleaned_data['group'])
            np.save()
            print("PITCH_ID: ")
            print(np.id)
            return redirect("/superuser/pitches/edit/" + str(np.id))
    
    context["form"] = PitchForm()
    return render(request,"website/admin_new_pitch.html",context)

def admin_delete_pitch(request,p_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    pitch = Pitch.objects.all().filter(id=p_id)
    pitch = pitch.first()
    if pitch == None:
        return HttpResponseNotFound("Pitch not found")
    dates = PitchDate.objects.all().filter(pitch=pitch)
    for d in dates:
        times = PitchTime.objects.all().filter(pitch_date=d)
        for t in times:
            t.delete()
        d.delete()
    pitch.delete()
    return redirect('/superuser/pitches')

def admin_edit_honours(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    ch = ClubHonour.objects.all()
    context['honours'] = ch
    return render(request,'website/admin_view_honours.html',context)

def admin_add_honour(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    if request.method == 'POST':
        form = ClubHonourForm(request.POST)
        if form.is_valid():
            h = form.cleaned_data['honour']
            d = form.cleaned_data['details']
            hnr = ClubHonour(honour=h,details=d)
            hnr.save()
            return redirect('/superuser/honours')
    context['form'] = HonourForm()
    return render(request,'website/admin_add_honour.html',context)

def admin_delete_honour(request,h_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    h = ClubHonour.objects.all().filter(id=h_id)
    if h.first() == None:
        return HttpResponseNotFound("The requested honour can't be found")
    h.delete()
    return redirect('/superuser/honours')

def admin_edit_sponsors(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    sponsors = Sponsor.objects.all()
    ag_sponsors = []
    age_groups = Team.objects.all()
    for ag in age_groups:
        ag_sponsors.append(AgeGroupSponsor.objects.all().filter(group=ag))
    context['sponsors'] = sponsors
    context['ag_sponsors'] = ag_sponsors
    context['age_groups'] = Team.objects.all()
    return render(request,'website/admin_edit_sponsors.html',context)
    
def admin_delete_sponsor(request,s_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    sp = Sponsor.objects.all().filter(id=s_id)
    if sp.first() == None:
        return HttpResponseNotFound("Sponsor not found")
    sp.delete()
    return redirect('/superuser/sponsors')

def admin_delete_sponsor_ag(request,s_id):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    sp = AgeGroupSponsor.objects.all().filter(id=s_id)
    if sp.first() == None:
        return HttpResponseNotFound("Sponsor not found")
    sp.delete()
    return redirect('/superuser/sponsors')

def admin_add_sponsor(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    if request.method == 'POST':
        form = SponsorForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            t = form.cleaned_data['team']
            u = form.cleaned_data['url']
            b = form.cleaned_data['banner']
            s = None
            if t == 'WJFC':
                s = Sponsor(banner=b,url=u)
            else:
                
                team=Team.objects.all().filter(id=t).first()
                s = AgeGroupSponsor(group=team,banner=b,url=u)
            s.save()
            return redirect("/superuser/sponsors")
    context['form'] = SponsorForm()
    return render(request,'website/admin_add_sponsor.html',context)

def admin_edit_clubhouse(request):
    return HttpResponse("OK")

def admin_edit_webmaster_news(request):
    context = getContext(request)
    if not context['isAdmin']:
        return HttpResponseForbidden(ERR_ADMIN)
    if request.method == 'POST':
        form = AgeGroupNewsForm(data=request.POST)
        ag_form = AgeGroupForm(data=request.POST)
        if(form.is_valid() and ag_form.is_valid()):
            grp=ag_form.cleaned_data['team']
            grp=Team.objects.all().filter(id=grp)
            grp=grp.first()
            text = form.cleaned_data["text"]
            title = form.cleaned_data["title"]
            agnws = AgeGroupNews(group=grp,title=title,text=text)
            agnws.save();
            return redirect('/personal') 
    form = AgeGroupNewsForm()
    ag_form = AgeGroupForm()
    context["form"] = form
    context["ag_form"] = ag_form
    return render(request, 'website/admin_webmaster_news.html',context)

def coach_delete_news(request, n_id):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    news = AgeGroupNews.objects.all().filter(group=grp, id=n_id)
    to_delete = news.first()
    if to_delete == None:
        return HttpResponseNotFound("The requested news doesn't exist!")
    news.delete()
    return redirect('/coach/view_news')

def coach_send_mail(request):
    context = getContext(request)
    if not context['isCoach']:
        return HttpResponseForbidden(ERR_COACH)
    grp = coachToTeam(request)
    mla = MailingListAddress.objects.all().filter(list=grp)
    if mla.first() == None:
        return HttpResponseNotFound("The Mailing list for age group " + grp.name + " is empty.")
        
    if request.method == 'POST':
        form = MailForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            subj = grp.name + ": " + form.cleaned_data['subject']
            msg = form.cleaned_data['text']
            sender = "wjfc.contacts@yandex.com"
            receivers = []
            for addr_obj in mla:
                addr = addr_obj.address
                receivers.append(addr)
                
            n = send_mail(subj,msg,sender,receivers)
            print("Sent:")
            print(n)
            redirect('/coach/mail_list')
    else:
        context['form'] = MailForm()
    context['group'] = grp
    return render(request, 'website/coach_send_mail.html',context)
