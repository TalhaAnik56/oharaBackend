from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register("genres", views.GenreViewSet)
router.register("writers", views.WriterViewSet)
router.register("books", views.BookViewSet, basename="book")

book_item_router = NestedDefaultRouter(router, "books", lookup="book")
book_item_router.register("bookitems", views.BookItemViewSet, basename="bookitem")

feedback_router = NestedDefaultRouter(router, "books", lookup="book")
feedback_router.register("feedbacks", views.FeedbackViewSet, basename="book-feedback")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(book_item_router.urls)),
    path("", include(feedback_router.urls)),
]
