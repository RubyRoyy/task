
from django.contrib import admin
from django.urls import path,include
from bank_loan_app import views

app_name = 'bank_loan_app'

urlpatterns = [
    path('',views.UserCreateView.as_view()),
    path('userlist/',views.UserList.as_view()),
    path('loan/',views.LoanView.as_view()),
    path('loan_detail/',views.LoanDetailView.as_view()),
    path('LoanStatus/',views.LoanStatusView.as_view())
]