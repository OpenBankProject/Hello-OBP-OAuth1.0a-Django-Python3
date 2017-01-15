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
    template_name = "transactions/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        transactions = []

        banks = api.get(self.request, '/banks')
        mybank = banks['banks'][0]['id']
        urlpath = u"/banks/{0}/accounts".format(mybank)
        accounts = api.get(self.request, urlpath)
        for a in accounts:
            try:
                eTrans = {}
                our_account = a['id']
                urlpath = u'/banks/{0}/accounts/{1}/owner/transactions'.format(mybank, our_account)
                trans = api.get(self.request, urlpath)
                
                urlpath = u'/banks/{0}/accounts/{1}/owner/transaction-request-types'.format(mybank,our_account)
                r = api.get(self.request, urlpath)
                challenge_type = r[0]['value']
                eTrans = {'id':our_account,'nrTrans':len(trans),'challenge_type':challenge_type}
                transactions.append(eTrans)
            except APIError as err:
                pass
                #messages.error(self.request, err)
                
        print(transactions)
            
        context.update({
            'transactions': transactions,
        })
        return context

