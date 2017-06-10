# Django
from django.test import TestCase
from django.contrib.auth.models import User
# Project
from ourAuth.forms import SignUpForm

class SignUpFormTestCase(TestCase):
    """
    Test cases for SignUpForm
    """
    
    def test_all_fields(self):
        """
        All fields filled
        Form should be valid 
        """
        form_data = { 
                'username': 'user', 
                'first_name': 'name', 
                'last_name': 'last_name', 
                'email': 'email@mail.com',
                'password1': 'password123',
                'password2': 'password123'
            }

        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_mandatory_fields(self):
        """
        Mandatory fields filled
        Form should be valid 
        """
        form_data = { 
                'username': 'user', 
                'email': 'email@mail.com',
                'password1': 'password123',
                'password2': 'password123'
            }

        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_different_password(self):
        """
        password1 and password2 are different
        """
        form_data = { 
                'username': 'user', 
                'first_name': 'name', 
                'last_name': 'last_name', 
                'email': 'email@mail.com',
                'password1': 'password13',
                'password2': 'passwor222'
            }

        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_email_unique(self):
        """
        Email must be unique
        """

        self.user = User.objects.create_user(
                        'temporary', 'temporary@gmail.com', 'temporary'
                    )

        form_data = { 
                'username': 'user', 
                'email': 'temporary@gmail.com',
                'password1': 'password123',
                'password2': 'password123'
            }

        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_username_empty(self):
        """
        username can not be empty
        """
        form_data = { 
                'email': 'email@mail.com',
                'password1': 'password123',
                'password2': 'password123'
            }

        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_email_empty(self):
        """
        email can not be empty
        """
        form_data = { 
                'username': 'user', 
                'password1': 'password123',
                'password2': 'password123'
            }

        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
