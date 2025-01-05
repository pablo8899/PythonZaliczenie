from django.forms import ValidationError
from django.test import TestCase
from datetime import date
from app.models import Product, UserProfile
from django.contrib.auth.models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("password123"))
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")

    def test_full_name(self):
        full_name = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(full_name, "Test User")


class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile = UserProfile.objects.create(user=self.user, birthdate=date(1990, 1, 1))

    def test_str_method(self):
        self.assertEqual(str(self.profile), "testuser")

    def test_user_relationship(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.user.userprofile, self.profile)

    def test_birthdate_field(self):
        self.assertEqual(self.profile.birthdate, date(1990, 1, 1))


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            price=99.99,
            description="This is a test product.",
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 99.99)
        self.assertEqual(self.product.description, "This is a test product.")
        self.assertFalse(self.product.image)

    def test_str_method(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_optional_fields(self):
        product_no_description = Product.objects.create(
            name="No Description Product",
            price=49.99,
        )
        self.assertIsNone(product_no_description.description)
        self.assertFalse(product_no_description.image)

    def test_price_validation(self):
        product_price_1 = Product.objects.create(name="Test price 1", price=20.01)
        product_price_2 = Product.objects.create(name="Test price 2", price=19.99)

        self.assertEqual(product_price_1.price, 20.01)
        self.assertEqual(product_price_2.price, 19.99)

    def test_invalid_price(self):
        product_with_negative_price = Product(name="Invalid Price Product", price=-10.00)
        with self.assertRaises(ValidationError):
            product_with_negative_price.full_clean()