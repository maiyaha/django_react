from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes   
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, generics
from .models import Book
from .serializers import BookSerializer
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from .modules.yolo_detection import detect
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'index.html')



@api_view(['GET'])
def helloAPI(request):
    return Response("hello world! 안녕하세요")

# 전체 도서 정보 조회 / 도서 등록
class BooksAPIMixins(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):  # GET 메소드 처리 함수 (전체 목록)
        return self.list(request, *args, **kwargs)  # mixins.ListModelMixin과 연결

    def post(self, request, *args, **kwargs):  # POST 메소드 처리 함수 (1권 등록)
        return self.create(request, *args, **kwargs)  # mixins.CreateModelMixin과 연결
    

#  도서 1권 조회(상세 도서 조회) / 수정 / 삭제
class BookAPIMixins(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "bookno"  # 기본키

    # GET : bookno 전달 받고, bookno에 해당되는 1개의 도서 정보 반환 (retrieve)
    def get(self, request, *args, **kwargs):  # GET 메소드 처리 함수 (1권 조회)
        return self.retrieve(request, *args, **kwargs)  # mixins.RetrieveModelMixin와 연결

    # PUT : bookno 전달 받고, bookno에 해당되는 1개의 도서 정보 수정 (update)
    def put(self, request, *args, **kwargs):  # PUT 메소드 처리 함수 (1권 수정)
        return self.update(request, *args, **kwargs)  # mixins.UpdateModelMixin와 연결

    # DELETE : bookno 전달 받고, bookno에 해당되는 1개의 도서 정보 삭제 (destroy)
    def delete(self, request, *args, **kwargs):  # DELETE 메소드 처리 함수 (1권 삭제)
        return self.destroy(request, *args, **kwargs)  # mixins.DestroyModelMixin와 연결

# 도서 검색
class BookSearchList(generics.ListAPIView):
    serializer_class = BookSerializer
    lookup_field = "bookname"

    # 검색어 1개인 경우
    # def get_queryset(self):
    #     print(self.kwargs["keyword"])  # path variable : keyword
    #     #  path("search/<str:keyword>/", BookSearchList.as_view()),여기서 <str:keyword>이 path varialbe
    #     # return Book.objects.filter(bookname=self.kwargs["keyword"]) # 완전 일치하는 경우

    #     return Book.objects.filter(
    #         bookname__contains=self.kwargs["value"]
    #     )  # 포함 여부 (와일드 검색)

    # keyword, value 2개인 경우
    def get_queryset(self):
        print(self.kwargs["type"])  # path variable : keyword
        print(self.kwargs["keyword"])
        #  path("search/<str:keyword>/", BookSearchList.as_view()),여기서 <str:keyword>이 path varialbe
        # return Book.objects.filter(bookname=self.kwargs["keyword"]) # 완전 일치하는 경우

        if self.kwargs["type"] == "bookname":
            # lookup_field = "bookname"
            return Book.objects.filter(
                bookname__contains=self.kwargs["keyword"]
            )  # 포함 여부 (와일드 검색)
        else:
            lookup_field = "bookauthor"
            return Book.objects.filter(bookauthor__contains=self.kwargs["keyword"])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# class BooksChart(generics.ListAPIView):
#     # queryset = Book.objects.all().order_by("-bookprice")
#     serializer_class = BookSerializer
#     lookup_field = "bookno"

#     # queryset = Book.objects.order_by("-bookprice").only("bookname", "bookprice")
#     # only() 안 됨
#     queryset = Book.objects.order_by("-bookprice")[:5] # TOP 5


#     # def get_queryset(self):
#     #     return Book.objects.only("bookname", "bookprice").order_by("-bookprice")

#     def get(self, request, *args, **kwargs):  # GET 메소드 처리 함수 (전체 목록)
#         return self.list(request, *args, **kwargs)
    
class BooksChart(generics.ListAPIView):
    serializer_class = BookSerializer
    
    # 내림차순 정렬 후 TOP 5
    queryset = Book.objects.order_by("-bookprice")[:5] 

    def get(self, request, *args, **kwargs):  # GET 메소드 처리 함수 
        return self.list(request, *args, **kwargs)


@api_view(['POST'])  
# @permission_classes([IsAuthenticated]) 
def file_upload_one(request):
    if request.method == "POST":
        file = request.FILES.get('imgFile')       
        fs = FileSystemStorage()

        # 파일명 중복되지 않도록 uuid 사용해서 파일명 변경
        uuid = uuid4().hex
        file_name = uuid + '_' +  file.name  
        
        fs.save(file_name, file)   # file.name, file 
        print(file_name)

        # 객체 탐지 함수 호출
        detect(file, file_name) # 이미지 객체와 파일명 전달 

    return Response(file_name)

