from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ResumeSection


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

    def test_signup_page_creates_user_and_redirects_repository(self):
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

        self.assertRedirects(response, reverse('repository'))
        self.assertTrue(get_user_model().objects.filter(email='ada@example.com').exists())

    def test_logged_in_nav_links_to_repository(self):
        user = get_user_model().objects.create_user(
            username='grace@example.com',
            email='grace@example.com',
            password='ComplexPassword123!',
            first_name='Grace',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('bullet_list'))

        self.assertContains(response, 'Hello Grace')
        self.assertContains(response, reverse('repository'))
        self.assertNotContains(response, 'Login</a>')
        self.assertNotContains(response, 'Sign up</a>')

    def test_repository_requires_login(self):
        response = self.client.get(reverse('repository'))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('repository')}")

    def test_repository_creates_default_sections_for_logged_in_user(self):
        user = get_user_model().objects.create_user(
            username='ada@example.com',
            email='ada@example.com',
            password='ComplexPassword123!',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('repository'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repository.html')
        self.assertContains(response, 'Document tabs')
        self.assertEqual(ResumeSection.objects.filter(user=user).count(), 5)

    def test_can_add_and_rename_section(self):
        user = get_user_model().objects.create_user(
            username='katherine@example.com',
            email='katherine@example.com',
            password='ComplexPassword123!',
        )
        self.client.force_login(user)

        add_response = self.client.post(reverse('add_section'), {'name': 'Certifications'})
        section = ResumeSection.objects.get(user=user, name='Certifications')
        self.assertRedirects(add_response, reverse('repository_section', args=[section.id]))

        update_response = self.client.post(
            reverse('update_section', args=[section.id]),
            {'name': 'Licenses & Certifications', 'notes': 'AWS and CPR'},
        )
        section.refresh_from_db()

        self.assertRedirects(update_response, reverse('repository_section', args=[section.id]))
        self.assertEqual(section.name, 'Licenses & Certifications')
        self.assertEqual(section.notes, 'AWS and CPR')
