from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Restaurant, Review


class RestaurantReviewTests(TestCase):
    """Tests for Restaurants and Reviews"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
        )
        cls.restaurant = Restaurant.objects.create(
            name="Qdoba",
        )
        cls.review = Review.objects.create(
            restaurant=cls.restaurant,
            author=cls.user,
            body="Nice body content",
            rating=5,  # Need to be one of the choices defined in model.
        )

    def test_restaurant_model(self):
        """Test Restaurant Model"""
        self.assertEqual(self.restaurant.name, "Qdoba")
        self.assertEqual(str(self.restaurant), "Qdoba")
        self.assertEqual(self.restaurant.get_absolute_url(), "/restaurant/1/")

    def test_review_model(self):
        """Test Review Model"""
        self.assertEqual(self.review.restaurant.name, "Qdoba")
        self.assertEqual(self.review.author.username, "testuser")
        self.assertEqual(self.review.body, "Nice body content")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(str(self.review), "Qdoba - testuser - 5")
        self.assertEqual(self.review.get_absolute_url(), "/review/1/")

    def test_url_exists_at_correct_location_restaurant_listview(self):
        """Test Restaurant List View has url"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_restaurant_detailview(self):
        """Test Restaurant List View has url"""
        response = self.client.get("/restaurant/1/")
        self.assertEqual(response.status_code, 200)

    def test_restaurant_listview(self):
        """Test Restaurant List View"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Qdoba")
        self.assertTemplateUsed(response, "home.html")

    def test_restaurant_detailview(self):
        """Test Restaurant Detail View"""
        response = self.client.get(
            reverse("restaurant_detail", kwargs={"pk": self.restaurant.pk})
        )
        no_response = self.client.get("/restaurant/100000/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Qdoba")
        self.assertContains(response, "Nice body content")
        self.assertContains(response, "5 out of 5")
        self.assertContains(response, "1 Reviews")
        self.assertTemplateUsed(response, "restaurant_detail.html")

    def test_review_detailview(self):
        """Test Review Detail View"""
        response = self.client.get(
            reverse("review_detail", kwargs={"pk": self.review.pk})
        )
        no_response = self.client.get("/review/100000/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Nice body content")
        self.assertContains(response, "5-Star")
        self.assertContains(response, "testuser")
        self.assertTemplateUsed(response, "review_detail.html")

    def test_review_createview(self):
        """Test Review Create View"""
        response = self.client.post(
            reverse("review_new", kwargs={"restaurant_pk": self.restaurant.pk}),
            {
                "restaurant": self.restaurant.id,
                "author": self.user.id,
                "body": "New text",
                "rating": 3,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.last().restaurant.name, self.restaurant.name)
        self.assertEqual(Review.objects.last().author.username, self.user.username)
        self.assertEqual(Review.objects.last().body, "New text")
        self.assertEqual(Review.objects.last().rating, 3)

    def test_review_updateview(self):
        """Test Review Update View"""
        response = self.client.post(
            reverse("review_edit", kwargs={"pk": self.review.pk}),
            {
                "body": "Update text",
                "rating": 3,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.last().restaurant.name, self.restaurant.name)
        self.assertEqual(Review.objects.last().author.username, self.user.username)
        self.assertEqual(Review.objects.last().body, "Update text")
        self.assertEqual(Review.objects.last().rating, 3)

    def test_review_deleteview(self):
        """Test Review Delete View"""
        response = self.client.post(
            reverse("review_delete", kwargs={"pk": self.review.pk})
        )
        self.assertEqual(response.status_code, 302)
