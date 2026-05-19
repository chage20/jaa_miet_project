from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Car, CarLike

User = get_user_model()


class CarModelTest(TestCase):
    """Тесты модели Car"""

    def test_car_creation(self):
        car = Car.objects.create(
            title='Toyota Camry 2.5',
            price=1500000,
            year=2020,
            engine_volume=2.5
        )
        self.assertEqual(car.title, 'Toyota Camry 2.5')
        self.assertEqual(car.price, 1500000)
        self.assertEqual(str(car), 'Toyota Camry 2.5')

    def test_car_string_representation(self):
        car = Car(title='Test Car', price=100000)
        self.assertEqual(str(car), 'Test Car')


class CarLikeTest(TestCase):
    """Тесты системы лайков"""

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

    def test_like_removal(self):
        """Пользователь может убрать лайк"""
        CarLike.objects.create(user=self.user, car=self.car)
        CarLike.objects.filter(user=self.user, car=self.car).delete()
        self.assertFalse(
            CarLike.objects.filter(user=self.user, car=self.car).exists()
        )

    def test_like_count(self):
        """Счётчик лайков работает корректно"""
        user2 = User.objects.create_user(username='user2', password='pass')
        CarLike.objects.create(user=self.user, car=self.car)
        CarLike.objects.create(user=user2, car=self.car)
        self.assertEqual(self.car.likes.count(), 2)


class CarsViewTest(TestCase):
    """Тесты представлений"""

    def setUp(self):
        self.client = Client()
        Car.objects.create(title='Test Car', price=100000, year=2019)

    def test_cars_page_status_code(self):
        """Страница /cars/ доступна"""
        response = self.client.get('/cars/')
        self.assertEqual(response.status_code, 200)

    def test_cars_page_template(self):
        """Используется правильный шаблон"""
        response = self.client.get('/cars/')
        self.assertTemplateUsed(response, 'cars.html')

    def test_cars_page_contains_car(self):
        """На странице отображаются автомобили"""
        response = self.client.get('/cars/')
        self.assertContains(response, 'Test Car')
        self.assertContains(response, '100000')