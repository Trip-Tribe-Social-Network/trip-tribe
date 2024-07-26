from django.test import TestCase
from account.forms import SignupForm

class SignupFormTest(TestCase):
    def test_signup_form_valid(self):
        form_data = {
            'email': 'validuser@example.com',
            'name': 'Valid User',
            'password1': 'password111',
            'password2': 'password111'
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        form_data = {
            'email': 'invaliduser@example.com',
            'name': 'Invalid User',
            'password1': 'password',
            'password2': 'differentpassword'
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
