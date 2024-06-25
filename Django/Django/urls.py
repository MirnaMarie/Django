"""
Definition of urls for Django.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.urls import re_path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('feedback/', views.feedback, name='feedback'),
    path('registration/', views.registration, name= 'registration'),
    path('blog/', views.blog, name= 'blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('child/', views.child, name= 'child'),
    path('family/', views.family, name= 'family'),
    path('extrim/', views.extrim, name= 'extrim'),
    path('newpost/', views.newpost, name= 'newpost'),
    path('basket/', views.basket, name= 'basket'),
    path('update_ticket_count/<int:ticket_index>/', views.update_ticket_count, name='update_ticket_count'),
    path('ticket-view/', views.ticket_view, name='ticket_view'),
    path('my_tickets/', views.my_tickets, name= 'my_tickets'),
    path('all_tickets/', views.all_tickets, name='all_tickets'),
    path('all_tickets_view/', views.all_tickets_view, name='all_tickets_view'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('shaker/', views.shaker, name= 'shaker'),
    path('katap/', views.katap, name= 'katap'),
    path('free/', views.free, name= 'free'),
    path('osminog/', views.osminog, name= 'osminog'),
    path('fire/', views.fire, name= 'fire'),
    path('aviat/', views.aviat, name= 'aviat'),
    path('katam/', views.katam, name= 'katam'),
    path('gonki/', views.gonki, name= 'gonki'),
    path('koleso/', views.koleso, name= 'koleso'),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()