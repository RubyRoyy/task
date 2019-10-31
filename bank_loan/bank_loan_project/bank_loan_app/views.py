import datetime
from  .models import ProfileData,LoanData
from .serializers import ProfileSerializers, UserSerializer, Loanserializer, LoanClearSerializer

from django.contrib.auth import authenticate
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

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

    def post(self, request):
        data = request.data
        serializer = Loanserializer(data=data)
        if serializer.is_valid():

            serializer.save()
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

    def put(self,request):
        data1 = ProfileData.objects.get(username=self.request.user)
        loan_statement = LoanData.objects.filter(username__username=data1).values('Loan_amount', 'Loan_period', 'status')
        data = request.data
        list_of_loan = len(loan_statement)
        if list_of_loan != 0:
            if loan_statement[list_of_loan-1]['status']==True:
                if len(data)==0:
                    loan_statement.update(loan_status=False)
                    return Response({'Loan status': "You cleared your loan"})
                else:
                    return Response({'Loan status':'You have already taken loan'})
        return Response({'Loan status': "You haven't taken any loan"})

