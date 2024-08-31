from django.test import TestCase
from post.forms import PostForm, AttachmentForm
from django.core.files.uploadedfile import SimpleUploadedFile
import base64


class PostFormTest(TestCase):
    def test_post_form_valid(self):
        form_data = {'body': 'Test Post'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

class AttachmentFormTest(TestCase):
    def test_attachment_form_valid(self):
        base64_image_data = (
            "iVBORw0KGgoAAAANSUhEUgAAAAUA"
            "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
            "9TXL0Y4OHwAAAABJRU5ErkJggg=="
        )
        image_data = base64.b64decode(base64_image_data)
        image = SimpleUploadedFile("test_image.png", image_data, content_type="image/png")

        form_data = {'image': image}
        form = AttachmentForm(data={}, files=form_data)
        self.assertTrue(form.is_valid())

    def test_attachment_form_invalid(self):
        form = AttachmentForm(data={})
        self.assertFalse(form.is_valid())
