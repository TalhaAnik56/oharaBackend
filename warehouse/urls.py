from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views


router=DefaultRouter()
router.register('genres',views.GenreViewSet)
router.register('writers',views.WriterViewSet)
router.register('books',views.BookViewSet)

urlpatterns=[
    path('',include(router.urls)),
    path('books/<int:pk>/feedbacks/',views.feedback_list)
]