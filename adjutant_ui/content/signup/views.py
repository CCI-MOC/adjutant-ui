# Copyright (c) 2016 Catalyst IT Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy

import json
from keystoneauth1.identity.v3 import OidcAccessToken
from keystoneauth1.session import Session
import requests

from horizon import forms

from adjutant_ui.content.signup import forms as su_forms

import os


class SignupFormView(forms.ModalFormView):
    form_class = su_forms.SignupForm
    submit_url = reverse_lazy("horizon:signup:signup:index")
    success_url = reverse_lazy("horizon:signup:signup:submitted")
    template_name = 'signup/index.html'

    def get_context_data(self, **kwargs):
        context = super(SignupFormView, self).get_context_data(**kwargs)

        access_token = self.request.META['OIDC_access_token']
        assert access_token

        auth = OidcAccessToken(auth_url=settings.OPENSTACK_KEYSTONE_URL,
                               identity_provider='moc',
                               protocol='openid',
                               access_token=access_token)
        session = Session(auth=auth)
        self.request.session['fernet_token'] = session.get_token()

        return context


def signup_sent_view(request):
    return render(request, 'signup/submitted.html')
