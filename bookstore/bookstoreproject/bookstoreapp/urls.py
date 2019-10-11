from django.urls import path
from .import views

urlpatterns=[
      path('',views.Bookslist.as_view()),
      path('<str:pk>/',views.BookView.as_view()),
      path('books/',views.BookDetails.as_view()),
#     path('book/',views.Bookview_Create.as_view()),
#     path('retrive/',views.Bookview_Retrive.as_view()),
#     path('update/',views.Bookview_Update.as_view()),
#     path('delete/',views.Bookview_Delete.as_view()),

]