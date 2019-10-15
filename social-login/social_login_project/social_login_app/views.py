from django.shortcuts import render
#from django.urls import reverse

from django.http import HttpResponse
from django.views.generic.base import TemplateView

class AboutUs(TemplateView):
    template_name = 'social-login.html'
        #return HttpResponse(reverse('social_login_app'))






