from django.db import models
from django.db.models import Avg
from django.urls import reverse

# Rating choices for the Review model.
RATING_CHOICES = [
    (5, "5-Star"),
    (4, "4-Star"),
    (3, "3-Star"),
    (2, "2-Star"),
    (1, "1-Star"),
]


class Restaurant(models.Model):
    """Restaurant Model"""

    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String"""
        return self.name

    def get_absolute_url(self):
        """Get absolute URL"""
        return reverse("restaurant_detail", kwargs={"pk": self.pk})

    def avg_rating(self):
        """Get the average rating"""
        return self.reviews.all().aggregate(Avg("rating"))["rating__avg"]

    def review_count(self):
        """Get the number of reviews"""
        return self.reviews.count()


class Review(models.Model):
    """Review Model"""

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    body = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String"""
        return f"{self.restaurant.name} - {self.name} - {self.rating}"

    def get_absolute_url(self):
        """Get absolute URL"""
        return reverse("review_detail", kwargs={"pk": self.pk})
