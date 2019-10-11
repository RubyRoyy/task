from django.urls import path
from .import views

urlpatterns=[
      path('',views.Bookslist.as_view()),
      path('<str:bookname>/',views.BookView.as_view()),

]