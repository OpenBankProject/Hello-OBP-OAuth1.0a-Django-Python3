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
    """Index view for payment"""
    template_name = "payment/index.html"



