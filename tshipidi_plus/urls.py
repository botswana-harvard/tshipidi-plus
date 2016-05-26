"""tshipidi_plus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from edc_registration.admin import registration_admin
from edc_call_manager.admin import call_manager_admin
from django_crypto_fields.admin import encryption_admin

from .views import (
    HomeView, StatisticsView, LoginView, LogoutView)
from django.views.generic.base import RedirectView

from .views import CallSubjectView

urlpatterns = [
    url(r'^admin/logout/', LogoutView.as_view(url='/login/')),
    url(r'^login/', LoginView.as_view(), name='login_url'),
    url(r'^logout/', LogoutView.as_view(url='/login/'), name='logout_url'),
    url(r'^accounts/login/', LoginView.as_view()),
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^statistics/', StatisticsView.as_view(), name='update-statistics'),
    url(r'^call_manager/$', RedirectView.as_view(url='/')),
    url(r'^call_manager/(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
        CallSubjectView.as_view(), name='call_subject'),
    url(r'^call_manager/(?P<app_label>\w+)/(?P<model_name>\w+)/',
        CallSubjectView.as_view(), name='call_subject'),
    url(r'^call_manager/', include('edc_call_manager.urls')),
    url(r'^encryption/$', RedirectView.as_view(url='/')),
    url(r'^encryption/', encryption_admin.urls),
    url(r'^admin/reg/$', RedirectView.as_view(url='/')),
    url(r'^admin/reg/', registration_admin.urls),
    url(r'^admin/cm/$', RedirectView.as_view(url='/')),
    url(r'^admin/cm/', call_manager_admin.urls),
    url(r'^admin/$', RedirectView.as_view(url='/')),
    url(r'^admin/', admin.site.urls),
    url(r'', HomeView.as_view(), name='default'),
]

admin.site.site_header = 'Tshipidi Plus'
admin.site.site_title = 'Tshipidi Plus'
admin.site.index_title = 'Tshipidi Plus Admin'
admin.site.site_url = '/'
