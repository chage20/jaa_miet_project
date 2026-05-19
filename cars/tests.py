from django.test import TestCase
from .models import Car, CarLike
from django.contrib.auth import get_user_model

User = get_user_model()


class CarModelTest(TestCase):
    """Тесты модели Car"""

    def test_car_creation(self):
        """Создание автомобиля"""
        car = Car.objects.create(
            title='Toyota Camry',
            price=1500000,
            year=2020,
            engine_volume=2.5
        )
        self.assertEqual(car.title, 'Toyota Camry')
        self.assertEqual(car.price, 1500000)
        self.assertEqual(car.year, 2020)
        self.assertEqual(car.engine_volume, 2.5)

    def test_car_string_representation(self):
        """Строковое представление (с годом)"""
        car = Car(title='Test Car', price=100000, year=2019)
        self.assertEqual(str(car), 'Test Car (2019)')


class CarLikeTest(TestCase):
    """Тесты лайков"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.car = Car.objects.create(
            title='Test Car',
            price=100000,
            year=2019
        )

    def test_like_creation(self):
        """Пользователь может поставить лайк"""
        CarLike.objects.create(user=self.user, car=self.car)
        self.assertTrue(
            CarLike.objects.filter(user=self.user, car=self.car).exists()
        )

    def test_like_count(self):
        """Счётчик лайков работает"""
        user2 = User.objects.create_user(username='user2', password='pass')
        CarLike.objects.create(user=self.user, car=self.car)
        CarLike.objects.create(user=user2, car=self.car)
        self.assertEqual(self.car.likes.count(), 2)