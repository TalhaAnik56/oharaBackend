from django.urls import path
from . import views

urlpatterns=[
    path('writers/',views.writer_list),
    path('writers/<int:pk>/',views.writer_details),
    path('genres/',views.genre_list),
    path('genres/<int:pk>/',views.genre_details),
    path('books/',views.book_list),
    path('books/<int:pk>/',views.book_details),
    path('books/<int:pk>/feedbacks/',views.feedback_list),
]