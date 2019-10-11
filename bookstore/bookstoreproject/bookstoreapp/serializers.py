from .models import BookstoreData
from rest_framework import serializers

class Bookstoreserializer(serializers.ModelSerializer):
    class Meta:
        model=BookstoreData
        fields="__all__"