from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "bookno",
            "bookname",
            "bookauthor",
            "bookprice",
            "bookdate",
            "bookstock",
            "pubno",
        ]
