# -*- coding: utf-8 -*-
"""
URLs for apimanager
"""

from django.conf.urls import url, include

from base.views import HomeView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^oauth/', include('oauth.urls')),
    url(r'^consumers/', include('consumers.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^transactions/', include('transactions.urls')),
    url(r'^payment/', include('payment.urls')),
    #url(r'^api_calls/', include('api_calls.urls')),
    #url(r'^api_config/', include('api_config.urls')),
]
