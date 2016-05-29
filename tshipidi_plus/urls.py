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


urlpatterns = [
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(pattern_name='login_url'), name='logout_url'),
    url(r'^statistics/', StatisticsView.as_view(), name='update-statistics'),
    url(r'^call_manager/$', RedirectView.as_view(pattern_name='home')),
    url(r'^call_manager/', include('edc_call_manager.urls', 'call_manager')),
    url(r'^admin/$', RedirectView.as_view(url='/')),
    # url(r'^admin/logout/', RedirectView.as_view(pattern_name='login_url')),
    # url(r'^accounts/login/', RedirectView.as_view(pattern_name='login_url')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/', call_manager_admin.urls),
    url(r'^admin/', registration_admin.urls),
    url(r'^admin/', encryption_admin.urls),
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^', HomeView.as_view(), name='home'),
]

admin.site.site_header = 'Tshipidi Plus'
admin.site.site_title = 'Tshipidi Plus'
admin.site.index_title = 'Tshipidi Plus Admin'
admin.site.site_url = '/'
