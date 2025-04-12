from django.test import TestCase, Client
from django.urls import reverse
from .models import *

# Create your tests here.
class AuthenticationViewsTests(TestCase):

    def setUp(self):
        # Создаем пользователя для тестов
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()

    # Проверка валидации верных данных при логине
    def test_login_user_post_valid(self):
        response = self.client.post(reverse('login'), data={'username': 'testuser', 'password': 'password123'})
        self.assertTrue('_auth_user_id' in self.client.session)

    # Проверка валидации неверных данных при логине
    def test_login_user_post_invalid(self):
        response = self.client.post(reverse('login'), data={'username': 'testuser', 'password': 'wrongpassword'})
        self.assertFalse('_auth_user_id' in self.client.session)

    # Проверка выхода из учетной записи
    def test_logout_user(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        self.assertFalse('_auth_user_id' in self.client.session)

    # Проверка регистрации
    def test_register_user_post_valid(self):
        city = Cities.objects.create(city='Горно-Алтайск', adress='г Горно-Алтайск')
        response = self.client.post(reverse('registration'), data={
            'username': 'registeruser',
            'password1': '2683399aQc+',
            'password2': '2683399aQc+',
            'gender': 'D',
            'birthday': '2025-01-27',
            'email': 'example@example.com',
            'city': 'Горно-Алтайск',
            'number': '',
            'food': '',
        })
        # self.assertRedirects(response, reverse('index'))
        self.assertTrue( User.objects.filter(username='registeruser').exists() )
        self.assertRedirects(response, reverse('profile'))