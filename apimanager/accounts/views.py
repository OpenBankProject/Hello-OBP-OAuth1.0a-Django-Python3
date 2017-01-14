# -*- coding: utf-8 -*-
"""
Views of consumers app
"""

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView

from base.api import api, APIError
from base.filters import BaseFilter, FilterTime


class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for consumers"""
    template_name = "accounts/index.html"
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        accounts = []

        try:
            
            banks = api.get(self.request, '/banks')
            mybank = banks['banks'][0]['id']
            urlpath = u"/banks/{0}/accounts".format(mybank)
            accounts = api.get(self.request, urlpath)
            for a in accounts:
                print (a['id'])
            #print(accounts)
            

        except APIError as err:
            messages.error(self.request, err)
            
        context.update({
            'accounts': accounts,
        })
        return context



