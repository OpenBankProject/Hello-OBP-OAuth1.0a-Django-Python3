# -*- coding: utf-8 -*-
"""
Views of consumers app
"""

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView
from random import randint

from base.api import api, APIError
from base.filters import BaseFilter, FilterTime
from .forms import PaymentForm

class IndexView(LoginRequiredMixin, TemplateView):
    """Index view for payment"""
    form_class = PaymentForm
    initial = {}
    template_name = "payment/index.html"
    
    def get(self, request, *args, **kwargs):
        banks = api.get(self.request, '/banks')
        mybank = banks['banks'][0]['id']
        urlpath = u"/banks/{0}/accounts".format(mybank)
        accounts = api.get(self.request, urlpath)
        self.initial['challenge_type'] = 'SANDBOX_TAN'
        self.initial['our_bank'] = banks['banks'][0]['id']
        self.initial['our_account_id'] = accounts[0]['id']
        self.initial['to_bank'] = banks['banks'][0]['id']
        self.initial['to_account_id'] = accounts[randint(1,len(accounts)-1)]['id']
        self.initial['currency'] = 'GBP'
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            data = form.cleaned_data
            payload = '{"to": {"account_id": "' + data['to_account_id'] +'", "bank_id": "' + data['to_bank'] + \
            '"}, "value": {"currency": "' + data['currency'] + '", "amount": "' + repr(data['value']) + '"}, "description": "Description abc", "challenge_type" : "' + \
            data['challenge_type'] + '"}'
            initiate_response = {}
            try:
                payment_url = u"/banks/{0}/accounts/{1}/owner/transaction-request-types/{2}/transaction-requests".format(data['our_bank'], data['our_account_id'], data['challenge_type'])

                print (u"payment_url is {0}".format(payment_url))

                print (u"payload is {0}".format(payload))

                initiate_response = api.post(request,payment_url,payload)
            except APIError as err:
                messages.error(self.request, err)
                #
            if "error" in initiate_response:
                messages.error(self.request,"Got an error: " + str(initiate_response))
            elif not "error" in initiate_response and len(initiate_response) > 0:
                messages.success(self.request, "Making payment successful")
                
            return HttpResponseRedirect('/payment')

        return render(request, self.template_name, {'form': form})



