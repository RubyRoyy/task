from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class ProfileData(models.Model):
    user=models.OneToOneField(User,on_delete=CASCADE)
    username=models.CharField(max_length=30)
    # password1=models.CharField(max_length=50)
    # password2=models.CharField(max_length=50)
    mobile=models.BigIntegerField()
    # email=models.EmailField(max_length=50,unique=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    def __str__(self):
        return self.username


class LoanData(models.Model):
    username=models.ForeignKey(ProfileData,on_delete=CASCADE)
    Loan_amount= models.IntegerField(default=10000)
    Loan_period=models.IntegerField(default=30)
    Date=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    Loan_STATUS=models.CharField(max_length=25,default='Available')

    def __str__(self):
        return str(self.username)



