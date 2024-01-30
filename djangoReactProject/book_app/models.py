from django.db import models

# Create your models here.

class Book(models.Model):
    bookno = models.CharField(db_column='bookNo', primary_key=True, max_length=10)  # Field name made lowercase.
    bookname = models.CharField(db_column='bookName', max_length=30)  # Field name made lowercase.
    bookauthor = models.CharField(db_column='bookAuthor', max_length=20)  # Field name made lowercase.
    bookprice = models.IntegerField(db_column='bookPrice', blank=True, null=True)  # Field name made lowercase.
    bookdate = models.DateField(db_column='bookDate', blank=True, null=True)  # Field name made lowercase.
    bookstock = models.IntegerField(db_column='bookStock', blank=True, null=True)  # Field name made lowercase.
    pubno = models.ForeignKey('Publisher', models.DO_NOTHING, db_column='pubNo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book'


class Publisher(models.Model):
    pubno = models.CharField(db_column='pubNo', primary_key=True, max_length=10)  # Field name made lowercase.
    pubname = models.CharField(db_column='pubName', max_length=20)  # Field name made lowercase.
    pub_phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'publisher'

