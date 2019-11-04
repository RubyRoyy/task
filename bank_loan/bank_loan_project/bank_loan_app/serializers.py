from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ProfileData, LoanData

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProfileData
        fields =('username','mobile','gender')

class UserSerializer(serializers.ModelSerializer):
    profiledata = ProfileSerializers(required=True)
    class Meta:
        model = User
        fields = ('username','password','email','profiledata')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        profile_data = validated_data.pop('profiledata')
        user = User.objects.create_user(**validated_data)
        profile = ProfileData.objects.create(
            user = user,
            username = profile_data['username'],
            mobile=profile_data['mobile'],
            gender =  profile_data['gender']
        )
        return user

class Loanserializer(serializers.ModelSerializer):

    class Meta:
        model=LoanData
        fields='__all__'

class LoanClearSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanData
        fields = ('status',)

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('email')
