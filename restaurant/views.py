from django.views.generic import ListView, DetailView

from .models import Restaurant, Review


class RestaurantListView(ListView):
    """List of Restaurants"""

    model = Restaurant
    template_name = "home.html"


class RestaurantDetailView(DetailView):
    """Detail of Restaurant"""

    model = Restaurant
    template_name = "restaurant_detail.html"
    context_object_name = "restaurant"
