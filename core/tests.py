from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthPageTests(TestCase):
    def test_home_links_to_separate_auth_pages(self):
        response = self.client.get(reverse('bullet_list'))

        self.assertContains(response, reverse('login'))
        self.assertContains(response, reverse('signup'))
        self.assertNotContains(response, 'id="account"')

    def test_login_page_renders_own_template(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, '<h1>Login</h1>', html=True)

    def test_signup_page_creates_user_and_redirects_home(self):
        response = self.client.post(
            reverse('signup'),
            {
                'first_name': 'Ada',
                'last_name': 'Lovelace',
                'email': 'ada@example.com',
                'password': 'ComplexPassword123!',
                'password_confirm': 'ComplexPassword123!',
            },
        )

        self.assertRedirects(response, reverse('bullet_list'))
        self.assertTrue(get_user_model().objects.filter(email='ada@example.com').exists())

    def test_logged_in_nav_greets_first_name(self):
        user = get_user_model().objects.create_user(
            username='grace@example.com',
            email='grace@example.com',
            password='ComplexPassword123!',
            first_name='Grace',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('bullet_list'))

        self.assertContains(response, 'Hello Grace')
        self.assertNotContains(response, 'Login</a>')
        self.assertNotContains(response, 'Sign up</a>')
