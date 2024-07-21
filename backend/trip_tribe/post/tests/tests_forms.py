from django.test import TestCase
from post.forms import PostForm

class PostFormTest(TestCase):
    def test_post_form_valid(self):
        form_data = {'body': 'Test Post'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
