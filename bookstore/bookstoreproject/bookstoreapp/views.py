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
    def get(self,request,bookname):
        books = BookstoreData.objects.get(pk=bookname)
        serializer = Bookstoreserializer(books)
        return Response(serializer.data , status=status.HTTP_200_OK)


    def post(self,request,pk):
        data1=BookstoreData.objects.get(pk=pk)
        data = request.data
        serializer = Bookstoreserializer(data1,data=data)

        if serializer.is_valid():
            serializer.save()
            # return Response({'message' : 'new object is added to Database'})
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class BookDetails(APIView):
    # def get_object(self,pk):
    #     try:
    #         books = BookstoreData.objects.get(pk=pk)
    #     except BookstoreData.DoesNotExist:
    #         books = None
    #     return books
    #
    #
    # def get(self,request):
    #     try:
    #         books = BookstoreData.objects.all()
    #     except BookstoreData.DoesNotExist:
    #         return Response({'msg': 'Record is not available..Try again'},
    #                        status=status.HTTP_404_NOT_FOUND)
    #     serializer = Bookstoreserializer(books)
    #     return Response(serializer.books , status=status.HTTP_200_OK)

    #
    # def put(self,request):
    #     books = self.get_object()
    #     if books is None:
    #         return Response({'msg': 'Record is not available to updating.Try again...'},
    #                         status=status.HTTP_404_NOT_FOUND)
    #
    #     serializer = Bookstoreserializer(books, data=request.data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data ,
    #                         status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors ,
    #                         status=status.HTTP_400_BAD_REQUEST)




    def delete(self,request):
        books = self.get_object()

        if books is None:
            return Response({'msg': 'Record is not available to Deleting.Try another record...'},
                            status=status.HTTP_404_NOT_FOUND)

        books.delete()
        return Response({'message' : 'Record deleted succefully'},
                        status = status.HTTP_204_NO_CONTENT)








# class Bookview_List(generics.ListAPIView):
#     queryset = BookstoreData.objects.all()
#     serializer_class = Bookstoreserializer
#
# class Bookview_Create(generics.CreateAPIView):
#     queryset = BookstoreData.objects.all()
#     serializer_class = Bookstoreserializer
#
# class Bookview_Retrive(generics.RetrieveAPIView):
#     queryset = BookstoreData.objects.all()
#     serializer_class = Bookstoreserializer
#
# class Bookview_Update(generics.UpdateAPIView):
#     queryset = BookstoreData.objects.all()
#     serializer_class = Bookstoreserializer
#
# class Bookview_Delete(generics.DestroyAPIView):
#     queryset = BookstoreData.objects.all()
#     serializer_class = Bookstoreserializer
#
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (JSONWebTokenAuthentication,)



