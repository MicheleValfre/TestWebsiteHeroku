from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Contact, JoinUsData, News, Player, Team

#SITE HEADER
admin.site.site_header = "WJFC Admin Page"

#CONTACTS
admin.site.register(Contact)

#JOIN-US FORM
class JoinUsDataAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'mail', 'phone')

admin.site.register(JoinUsData,JoinUsDataAdmin)

#NEWS FORM
class NewsAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(News,NewsAdmin)

#PLAYER FORM
admin.site.register(Player)

#TEAM FORM
admin.site.register(Team)

#============================
