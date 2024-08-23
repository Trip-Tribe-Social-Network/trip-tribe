from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from account.forms import ProfileForm, SignupForm
from account.models import User
import base64

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

class ProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='strongpassword123'
        )

    def test_profile_form_valid(self):
        base64_image_data = (
            "iVBORw0KGgoAAAANSUhEUgAAAAUA"
            "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
            "9TXL0Y4OHwAAAABJRU5ErkJggg=="
        )
        image_data = base64.b64decode(base64_image_data)
        avatar = SimpleUploadedFile("test_image.png", image_data, content_type="image/png")
        form_data = {
            'email': 'newemail@example.com',
            'name': 'New Name',
        }
        files = {
            'avatar': avatar
        }
        form = ProfileForm(data=form_data, files=files, instance=self.user)

        self.assertTrue(form.is_valid())
        
        form.save()
        self.user.refresh_from_db()

        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(self.user.name, 'New Name')
        self.assertTrue(self.user.avatar.name.startswith('avatars/test_image'))

    def test_profile_form_invalid(self):
        form_data = {
            'email': 'invalidemail',    
            'avatar': None
        }
        form = ProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors.get('email', []))

    def test_profile_form_with_no_avatar(self):
        form_data = {
            'email': 'anotheremail@example.com',
            'name': 'Another Name',
        }
        form = ProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'anotheremail@example.com')
        self.assertEqual(self.user.name, 'Another Name')
        self.assertEqual(self.user.avatar.name, '', "Avatar name should be an empty string if no file is uploaded.")
