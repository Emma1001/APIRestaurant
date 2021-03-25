import tempfile

from django.test import TestCase
import io

from PIL import Image
from rest_framework.test import APIClient

from users.models import User


class TestCaseUser(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user')
        self.client = APIClient()

    def test_upload_image(self):
        self.client.force_authenticate(self.user)
        url = '/users/%s/upload-image/' % self.user.pk

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(tmp_file)
        tmp_file.seek(0)

        response = self.client.post(url, {'image': tmp_file}, format='multipart')

        self.assertEqual(response.status_code, 200)

    def test_upload_image_wrong_suffix(self):
        self.client.force_authenticate(self.user)
        url = '/users/%s/upload-image/' % self.user.pk

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.gif')
        image.save(tmp_file)
        tmp_file.seek(0)

        response = self.client.post(url, {'image': tmp_file}, format='multipart')

        self.assertEqual(response.status_code, 400)

