"""
Core tests
"""

# from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import LoginForm, SignupForm
from .models import UserProfile

# from rest_framework.test import APIClient
User = get_user_model()


class UserProfileTest(TestCase):
    """
    Test the UserProfile model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data
        """
        User.objects.create_user(
            email='test@gmail.com', password='test54321'
        )

    def setUp(self):
        # self.client = APIClient()
        """
        Set up each test method
        """
        self.user = User.objects.get(username='test', email='test@gmail.com')

    def test_create_userprofile(self):
        """
        Test creating a user profile
        """
        userprofile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.assertTrue(isinstance(userprofile, UserProfile))
        self.assertEqual(userprofile.user, self.user)
        self.assertEqual(userprofile.bio, None)
        self.assertEqual(
            userprofile.img, 'https://via.placeholder.com/100x100x.jpg'
        )
        self.assertEqual(
            userprofile.__str__(), self.user.username or self.user.email
        )
        self.assertEqual(userprofile.user.is_student, True)
        self.assertEqual(userprofile.user.is_instructor, False)
        # self.assertEqual(userprofile.bio.placeholder, 'Bio')

    def test_update_userprofile(self):
        '''
        Test updating a user profile
        '''
        userprofile, _ = UserProfile.objects.get_or_create(user=self.user)
        userprofile.bio = 'Test Bio'
        userprofile.img = 'https://via.placeholder.com/100x100x.jpg'
        userprofile.save()
        self.assertEqual(userprofile.bio, 'Test Bio')
        self.assertEqual(
            userprofile.img, 'https://via.placeholder.com/100x100x.jpg'
        )

class CoreViewsTest(TestCase):
    """
    Test the core views
    """

    @classmethod
    def setUpTestData(cls):
        """
        Test the test data for core views
        """
        get_user_model().objects.create_user(
            username='test', email='test@gmail.com', password='test54321'
        )

    def setUp(self):
        """
        Set up each test method
        """
        self.user = get_user_model().objects.get(email='test@gmail.com')

    def test_login_view(self):
        """
        Test the login view
        """
        url = reverse('core:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        '''self.assertTemplateUsed(response, 'core/registration/form.html')
        self.assertContains(response, 'Log in')
        data = {'username': 'test@gmail.com', 'password': 'test54321'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))'''

    def test_signup_view(self):
        """
        Test the sign-up view.
        """
        url = reverse('core:signup')
        response = self.client.get(url, follow=True)

        # Use another request to confirm the template and contents
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'core/registration/form.html')
        """self.assertContains(response, 'Sign up')
        self.assertContains(response, 'Already have an account?')

        data = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password1': 'test54321',
            'password2': 'test54321',
        }
        response = self.client.post(url, data)
        # self.assertRedirects(response, reverse('index'))
        # self.assertEqual(response.status_code, 302)  # Expecting a redirect after a successful post

        user = get_user_model().objects.get(email='test@gmail.com')
        self.assertTrue(
            user.is_active
        )  # user.is_active should be False initially until email confirmation
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertTrue(
            user.check_password('test54321')
        )  # Correct way to check password
        """

    def test_logout_view(self):
        """
        Test the logout view
        """
        url = reverse('core:logout')
        response = self.client.post(url)
        # self.assertRedirects(response, settings.LOGOUT_REDIRECT_URL)
        self.assertEqual(response.status_code, 302)

class FormsTest(TestCase):
    """
    Test the forms
    """

    @classmethod
    def setUpTestData(cls):
        """
        Test the test data for forms
        """
        get_user_model().objects.create_user(
            username='test',
            email='test@gmail.com',
            password='test54321',
            is_student=True,
            is_instructor=False,
        )

    def setUp(self):
        """
        Set up each test method
        """
        self.user = get_user_model().objects.get(email='test@gmail.com')

    def test_login_form_valid(self):
        """
        Test the login form valid
        """
        data = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'test54321',
        }

        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'test')
        self.assertEqual(form.cleaned_data['password'], 'test54321')

    def test_login_form_invalid(self):
        """
        Test the login form invalid
        """
        data = {'username': 'test', 'password': 'test12345'}
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['__all__'])

    def test_signup_form_valid(self):
        """
        Test the signup form valid
        """
        data = {
            'email': 'test15@gmail.com',
            'password1': 'test54321',
            'password2': 'test54321',
        }
        form = SignupForm(data=data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], 'test15@gmail.com')
        self.assertTrue(
            form.cleaned_data['password1'] == form.cleaned_data['password2']
        )

    def test_signup_form_invalid(self):
        """
        Test the form invalid
        """
        data = {
            'email': 'test15@gmail.com',
            'password1': 'test54321',
            'password2': 'wrong54321',
        }
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
