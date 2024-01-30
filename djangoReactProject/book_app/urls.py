from django.urls import path
from .views import helloAPI, BooksAPIMixins, BookAPIMixins,\
BookSearchList, BooksChart, file_upload_one, index

urlpatterns = [
    path('', index, name='index'),
    path("hello/", helloAPI),
    path("books/", BooksAPIMixins.as_view()),
    path("book/<str:bookno>/", BookAPIMixins.as_view()),
    path("search/<str:type>/<str:keyword>/", BookSearchList.as_view()),
    path("chart_db/", BooksChart.as_view()),
    path("upload/", file_upload_one),
]