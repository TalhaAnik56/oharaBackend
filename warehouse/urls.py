from django.urls import path
from . import views

urlpatterns=[
    path('writers/',views.writer_list),
    path('writers/<int:pk>',views.writer_details),
    path('books/',views.book_list),
    path('books/<int:pk>',views.book_details)
]