from django.urls import path

from .views import (
    RestaurantListView,
    RestaurantDetailView,
    ReviewCreateView,
    ReviewDetailView,
    ReviewDeleteView,
    ReviewUpdateView,
)

urlpatterns = [
    path(
        "restaurant/<int:restaurant_pk>/review/new/",
        ReviewCreateView.as_view(),
        name="review_create",
    ),
    path(
        "review/<int:pk>/detail/",
        ReviewDetailView.as_view(),
        name="review_detail",
    ),
    path(
        "review/<int:pk>/edit/",
        ReviewUpdateView.as_view(),
        name="review_edit",
    ),
    path(
        "review/<int:pk>/delete/",
        ReviewDeleteView.as_view(),
        name="review_delete",
    ),
    path(
        "restaurant/<int:pk>/",
        RestaurantDetailView.as_view(),
        name="restaurant_detail",
    ),
    path("", RestaurantListView.as_view(), name="home"),
]
