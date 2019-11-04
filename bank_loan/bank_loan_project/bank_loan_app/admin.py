from django.contrib import admin
from .models import ProfileData, LoanData, EmailData

admin.site.register(ProfileData)
admin.site.register(LoanData)
admin.site.register(EmailData)