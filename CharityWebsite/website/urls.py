from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logoutFunction, name='logout'),
    path('events', views.events, name='events'),
    path('events/tournaments', views.tournaments, name='tournaments'),
    path('events/fundraising', views.fundraising, name='fundraising'),
    path('sponsors', views.sponsors, name='sponsors'),
    path('welfare', views.welfare, name='welfare'),
    path('welfare/policies', views.welfare_policies, name='welfare_policies'),
    path('teams', views.teams, name='teams'),
    path('about/priv', views.privacy_policy, name='privacy_policy'),
    path('about/docs', views.documents_and_policies, name='documents_and_policies'),
    path('teams/general_info', views.general_info, name='general_info'),
    path('teams/coach_contacts', views.coach_contacts, name='coach_contacts'),
    path('teams/age_group_sponsor', views.age_group_sponsor, name='age_group_sponsor'),
    #ABOUT TAB
    path('about', views.about, name='about'),
    path('about/contacts', views.contacts, name='contacts'),
    path('about/ethos', views.ethos, name='ethos'),
    path('about/news', views.news, name='news'),
    path('about/3g-astro', views.astro, name='astro'),
    path('about/directions', views.directions, name='directions'),
    path('about/calendar', views.CalendarView.as_view(), name='calendar'),
    path('about/joinus', views.joinus, name='joinus'),
    path('about/welfare', views.welfare, name='welfare'),
    path('edit-contacts', views.editContacts, name='editcontacts'),
    #PERSONAL TAB
    path('personal', views.dashboard, name='dashboard'),
    #COACH TAB
    path('coach/edit_welcome', views.coach_edit_welcome, name='coach_edit_welcome'),
    path('coach/view_news', views.view_news, name='coach_view_news'),
    path('coach/edit_news', views.coach_edit_news, name='coach_edit_news'),
    path('coach/delete_news/<int:n_id>/', views.coach_delete_news, name="coach_delete_news"),
    path('coach/edit_team_contacts', views.coach_edit_contacts, name="coach_edit_contacts"),
    path('coach/delete_contact/<int:c_id>/', views.coach_delete_contact, name="coach_delete_contact"),
    path('coach/edit_contact/<int:c_id>/', views.coach_edit_contact, name="coach_edit_contact"),

    path('coach/add_contact', views.coach_add_contact, name="coach_add_contact"),
    path('coach/mail_list', views.coach_edit_mail_list, name="coach_edit_mail_list"),
    path('coach/add_mail', views.coach_add_mail, name="coach_add_mail"),
    path('coach/delete_mail/<int:m_id>', views.coach_delete_mail, name="coach_delete_mail"),
    path('coach/send_mail/', views.coach_send_mail, name="coach_send_mail"),
    path('coach/team_downloads', views.coach_team_downloads, name="coach_team_downloads"),
    path('coach/add_download', views.coach_add_download , name="coach_add_download"),
    path('coach/delete_download/<int:d_id>', views.coach_delete_download, name="coach_delete_download"),
    path('coach/training', views.coach_view_training, name="coach_view_training"),
    path('coach/training/edit_text', views.coach_edit_training, name="coach_edit_training"),
    path('coach/training/upload_resource', views.coach_add_training_resource, name="coach_add_training_resource"),
    path('coach/training/delete_resource/<int:r_id>', views.coach_remove_training_resource, name="coach_remove_training_resource"),
    path('coach/honours', views.coach_view_honours, name="coach_view_honours"),
    path('coach/add_honour',views.coach_add_honour, name="coach_add_honour"),
    path('coach/delete_honour/<int:h_id>', views.coach_delete_honour, name="coach_delete_honour"),
    path('coach/players', views.coach_view_players, name="coach_view_players"),
    path('coach/add_player',views.coach_add_player, name="coach_add_player"),
    path('coach/delete_player/<int:p_id>', views.coach_delete_player, name="coach_delete_player"),
    path('coach/fixtures', views.coach_view_fixtures, name="coach_view_fixtures"),
    path('coach/add_fixture',views.coach_add_fixture, name="coach_add_fixture"),
    path('coach/delete_fixture/<int:f_id>', views.coach_delete_fixture, name="coach_delete_fixture"),
    path('coach/pitches', views.coach_view_pitches, name="coach_view_pitches"),
    path('coach/view_pitch/<int:p_id>', views.coach_view_pitch, name="coach_view_pitch"),
    path('coach/book_pitch/<int:p_id>', views.coach_book_pitch, name="coach_book_pitch"),
    path('coach/unbook_pitch/<int:p_id>', views.coach_unbook_pitch, name="coach_unbook_pitch"),



    path('coach/add_pitch',views.coach_add_pitch, name="coach_add_pitch"),
    path('coach/delete_pitch/<int:p_id>', views.coach_delete_pitch, name="coach_delete_pitch"),
    path('fixture_details/<int:f_id>', views.details_fixture, name="details_fixture"),
    #PARENT TAB
    path('parent/downloads',views.parent_view_downloads,name="parent_view_downloads"),
    path('parent/news',views.parent_view_news, name="parent_view_news"),
    path('parent/contacts',views.parent_view_contacts, name="parent_view_contacts"),
    path('parent/training',views.parent_view_training, name="parent_view_training"),
    path('parent/fixtures',views.parent_view_fixtures, name="parent_view_fixtures"),
    path('parent/fixtures/teams/<int:f_id>',views.parent_fixture_teams, name="parent_fixture_teams"),
    path('parent/players',views.parent_view_players, name="parent_view_players"),
    path('parent/honours',views.parent_view_honours, name="parent_view_honours"),
    path('parent/emails',views.parent_mail_list_subscribe, name="parent_mail_list_subscribe"),
    path('parent/emails/delete/<int:m_id>',views.parent_mail_list_unsubscribe, name="parent_mail_list_unsubscribe"),
    #SUPERUSER TAB
    path('superuser/edit_info',views.admin_edit_info, name="admin_edit_info"),
    path('superuser/about',views.admin_edit_about, name="admin_edit_about"),
    path('superuser/ethos',views.admin_edit_ethos, name="admin_edit_ethos"),
    path('superuser/3g_astro',views.admin_edit_3g_astro, name="admin_edit_3g_astro"),
    path('superuser/welfare',views.admin_edit_welfare, name="admin_edit_welfare"),
    path('superuser/welcome', views.admin_edit_welcome, name="admin_edit_welcome"),
    path('superuser/news', views.admin_edit_news, name="admin_edit_news"),
    path('superuser/news_img/<int:n_id>', views.admin_add_news_img, name="admin_news_image"),
    path('superuser/delete_img/<int:n_id>/<int:i_id>', views.admin_del_news_img, name="admin_del_news_img"),
    path('superuser/create_news', views.admin_create_news , name="admin_create_news"),
    path('superuser/delete_news/<int:n_id>', views.admin_delete_news, name="admin_delete_news"),
    path('superuser/contacts', views.admin_edit_contacts, name="admin_edit_contacts"),
    path('superuser/contacts/edit/<int:c_id>', views.admin_edit_contact, name="admin_edit_contact"),
    path('superuser/add_contact', views.admin_add_contact, name="admin_add_contact"),
    path('superuser/delete_contact/<int:c_id>', views.admin_delete_contact, name="admin_delete_contact"),
    path('superuser/downloads', views.admin_edit_downloads, name="admin_edit_downloads"),
    path('superuser/add_download', views.admin_add_download, name="admin_add_download"),
    path('superuser/delete_download/<int:d_id>', views.admin_delete_download, name="admin_delete_download"),
    path('superuser/players', views.admin_edit_players, name="admin_edit_players"),
    path('superuser/add_player', views.admin_add_player, name="admin_add_player"),
    path('superuser/delete_player/<int:p_id>', views.admin_delete_player, name="admin_delete_player"),
    path('superuser/events', views.admin_edit_events, name="admin_edit_events"),
    path('superuser/add_tournament', views.admin_add_tournament, name="admin_add_tournament"),
    path('superuser/add_foundraising', views.admin_add_foundraising, name="admin_add_foundraising"),
    path('superuser/emails', views.admin_view_emails, name="admin_view_emails"),
    path('superuser/pitches', views.admin_edit_pitches, name="admin_edit_pitches"),
    path('superuser/pitches/new', views.admin_new_pitch, name="admin_new_pitch"),
    path('superuser/pitches/edit/<int:p_id>', views.admin_edit_pitch,name="admin_edit_pitch"),
    path('superuser/pitches/add_date/<int:p_id>', views.admin_pitch_add_date,name="admin_pitch_add_date"),
    path('superuser/pitches/delete_date/<int:p_id>', views.admin_pitch_delete_date,name="admin_pitch_delete_date"),
    path('superuser/pitches/add_time/<int:p_id>', views.admin_pitch_add_time,name="admin_pitch_add_time"),
    path('superuser/pitches/delete/<int:p_id>', views.admin_delete_pitch, name="admin_delete_pitch"),
    path('superuser/honours', views.admin_edit_honours, name="admin_edit_honours"),
    path('superuser/add_honour', views.admin_add_honour, name="admin_add_honour"),
    path('superuser/delete_honour/<int:h_id>',views.admin_delete_honour,name="admin_delete_honour"),
    path('superuser/sponsors', views.admin_edit_sponsors, name="admin_edit_sponsors"),
    path('superuser/add_sponsor', views.admin_add_sponsor, name="admin_add_sponsor"),
    path('superuser/delete_sponsor/<int:s_id>', views.admin_delete_sponsor, name="admin_delete_sponsor"),
    path('superuser/delete_sponsor_ag/<int:s_id>', views.admin_delete_sponsor_ag, name="admin_delete_sponsor_ag"),
    path('superuser/clubhouse', views.admin_edit_clubhouse, name="admin_edit_clubhouse"),
    path('superuser/webmaster_news', views.admin_edit_webmaster_news, name="admin_edit_webmaster_news"),
    path('superuser/send_mail/<int:m_id>', views.admin_send_mail, name="admin_send_mail")
]
