from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Restaurant, Review


class RestaurantListView(ListView):
    """List of Restaurants"""

    model = Restaurant
    template_name = "home.html"


class RestaurantDetailView(DetailView):
    """Detail of Restaurant with list of Reviews"""

    model = Restaurant
    template_name = "restaurant_detail.html"
    context_object_name = "restaurant"


class ReviewCreateView(CreateView):
    """Review Create View"""

    model = Review
    template_name = "review_new.html"
    fields = ["restaurant", "author", "body", "rating"]

    def get_initial(self):
        """Get the initial data for the form"""
        self.restaurant = get_object_or_404(
            Restaurant,
            pk=self.kwargs.get("restaurant_pk"),
        )

        return {
            "restaurant": self.restaurant,
            "author": self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["restaurant"] = self.restaurant
        return context


class ReviewDetailView(DetailView):
    """Detail of Review"""

    model = Review
    template_name = "review_detail.html"
    context_object_name = "review"


class ReviewUpdateView(UpdateView):
    """Review Create View"""

    model = Review
    template_name = "review_edit.html"
    fields = ["body", "rating"]


class ReviewDeleteView(DeleteView):
    """Review Create View"""

    model = Review
    template_name = "review_delete.html"
    success_url = reverse_lazy("home")
