# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class PaymentForm(forms.Form):
    our_bank = forms.CharField(required = True)
    our_account_id = forms.CharField(required = True)
    value = forms.FloatField(required = True, help_text = ('<= 1000'))
    currency = forms.CharField(required = True)
    to_bank = forms.CharField(required = True)
    to_account_id = forms.CharField(required = True)
    challenge_type = forms.CharField(required = True)
    
    def clean_value(self):
        cleaned_data = super(PaymentForm, self).clean()
        value = cleaned_data.get('value')
        if value>1000:
            raise forms.ValidationError(
                    "only value <= 1000 accepted"
                )
        return cleaned_data