from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from .models import BookstoreData
from .serializers import Bookstoreserializer
from rest_framework.response import Response
from  rest_framework import status
import json


class Bookslist(APIView):

    def get(self,request):
        data=BookstoreData.objects.all()
        serializer = Bookstoreserializer(data,many=True)
        return Response(serializer.data)

    def post(self,request):
        data=request.data
        serializer=Bookstoreserializer(data=data)
        if serializer.is_valid():
            BookstoreData.objects.create(**data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class BookView(APIView):



    def get(self, request, bookname):
        try:
            books = BookstoreData.objects.get(pk=bookname)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Bookstoreserializer(books)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self,request,bookname):
        try:
            data1=BookstoreData.objects.get(pk=bookname)
        except:
            return Response({'msg':"record not found"},status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = Bookstoreserializer(data1,data=data)

        if serializer.is_valid():
            serializer.save()
            # return Response({'message' : 'new object is added to Database'})
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)













