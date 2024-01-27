from django.urls import path
from . import views

urlpatterns=[
    path('writers/',views.WriterList.as_view()),
    path('writers/<int:pk>/',views.WriterDetails.as_view()),
    path('genres/',views.GenreList.as_view()),
    path('genres/<int:pk>/',views.GenreDetails.as_view()),
    path('books/',views.BookList.as_view()),
    path('books/<int:pk>/',views.BookDetails.as_view()),
    path('books/<int:pk>/feedbacks/',views.feedback_list)
]