from django.db import models

class BookstoreData(models.Model):
    bookname=models.CharField(max_length=50,primary_key=True)
    author=models.CharField(max_length=30)
    publisheddate=models.DateField()
    number_of_books=models.IntegerField()
    rack=models.IntegerField()

    def __str__(self):
        return self.bookname