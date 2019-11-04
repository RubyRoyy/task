import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import ProfileData, LoanData, EmailData
from .serializers import UserSerializer, Loanserializer, LoanClearSerializer


class UserCreateView(APIView):

    def get(self, request):
        data = request.data
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoanView(APIView):
    serializer_class = Loanserializer

    def get(self, request):
        serializer = Loanserializer(request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self,request):
        data1 = ProfileData.objects.get(username=self.request.user)
        loan_stat = LoanData.objects.filter(username__username=data1).values('status')
        det = len(loan_stat)
        if det != 0:
            det = det-1
            if loan_stat[det]['status'] == True:
                return Response({'msg': "Please first clear the taken loan before taking another loan"})
        data = request.data
        serializer = Loanserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            alert_date = datetime.date.today()+datetime.timedelta(days=serializer.data['Loan_period']-1)
            Email=EmailData.objects.create(username=data1,Alert_Date=alert_date)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanDetailView(APIView):
    def get(self,request):
        data1=ProfileData.objects.get(username=self.request.user)
        data=LoanData.objects.filter(username__username=data1).values('Loan_amount','Loan_period','status')
        return Response(data)

class LoanStatusView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanClearSerializer


    def get(self,request):
        data1 = ProfileData.objects.get(username=self.request.user)
        loan_statement = LoanData.objects.filter(username__username=data1).values('Loan_amount','Loan_period','status','Date')
        list_of_loan = len(loan_statement)
        if list_of_loan !=0:
            if loan_statement[list_of_loan-1]['status'] == True:
                total_days = datetime.date.today()-loan_statement[list_of_loan-1]['Date']
                Actual_due_date= loan_statement[list_of_loan-1]['Date']+datetime.timedelta(days=loan_statement[list_of_loan-1]['Loan_period'])
                if total_days.days <= loan_statement[list_of_loan-1]['Loan_period']:
                    remaining_days =  loan_statement[list_of_loan-1]['Loan_period'] - total_days.days
                else:
                    remaining_days =  total_days.days - loan_statement[list_of_loan-1]['Loan_period']
                amount=loan_statement[list_of_loan-1]['Loan_amount']
                r=0.6
                t=(1/365)
                SI_day= (amount*r*t)/100
                Total_day=SI_day*total_days.days
                principal_amount = amount+Total_day
                if total_days.days < loan_statement[list_of_loan-1]['Loan_period']:
                    return Response({'Total amount to be paid':principal_amount,
                                     'Number of days left to pay loan': str(remaining_days)+' days',
                                     'Due date':Actual_due_date})
                elif total_days.days == loan_statement[list_of_loan-1]['Loan_period']:
                    return Response({'Total amount to be paid':principal_amount,
                                     'Number of days left to pay loan': str(remaining_days)+' days',
                                     'Loan status':'Last day to pay loan',
                                     'Due date':str(Actual_due_date)+'(today)'})
                else:
                    return Response({'Total amount to be paid till date': principal_amount,
                                     'Number of days crossed after the loan due period': str(remaining_days) + ' days',
                                     'Loan status':'Your loan period has been crossed',
                                     'Due date':Actual_due_date})
            return Response({'Loan status':'You do not have any active loan'})
        return Response({'Loan status': "You haven't taken any loan"})


    def post(self, request):
        data1 = ProfileData.objects.get(username=self.request.user)
        loan_statement = LoanData.objects.filter(username=data1).values('Loan_amount', 'Loan_period', 'status', 'Date',
                                                                   'Loan_STATUS')
        data = request.data
        serializer = LoanClearSerializer(data=data)
        serializer.is_valid()
        dat = serializer.data['status']
        list_of_loan = len(loan_statement)
        if dat == True and loan_statement[list_of_loan - 1]['status'] == True:
            if list_of_loan != 0:
                loan_stats = LoanData.objects.filter(username=data1)[list_of_loan - 1]
                total_days = datetime.date.today() - loan_stats.Date
                if total_days.days < loan_stats.Loan_period:
                    loan_stats.Loan_STATUS = 'Foreclosed'
                    loan_stats.status = False
                    loan_stats.save()
                    return Response({'Loan Status': loan_stats.Loan_STATUS})
                elif total_days.days == loan_stats.Loan_period:
                    loan_stats.Loan_STATUS = 'Disbursed'
                    loan_stats.status = False
                    loan_stats.save()
                    return Response({'Loan Status': loan_stats.Loan_STATUS})
                else:
                    loan_stats.Loan_STATUS = 'Defaulter'
                    loan_stats.status = False
                    loan_stats.save()
                    return Response({'Loan Status': loan_stats.Loan_STATUS})
        return Response({"Loan status": "You don't have any active loan"})

def email(request):
    Email=EmailData.objects.filter(Alert_Date=datetime.date.today())
    recipient_list = []
    for e in Email:
        data = LoanData.objects.filter(username=e.username)
        l=len(data)
        if data[l-1].status == True:
            data1=User.objects.get(username=e.username)
            recipient_list.append(data1.email)

    print(recipient_list)
    subject = 'Loan message!!!'
    message = 'Hello !! Your loan period will expire Tomorrow .Please pay as soon as possible'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list)
    return HttpResponse({'Email sent'})

