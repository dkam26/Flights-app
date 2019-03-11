from django.test import TestCase

# Create your tests here.
from .models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
import json
from PIL import Image
import tempfile
from .backends import MyAuthBackend


class ModelTestCase(TestCase):
    def setUp(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        with open(tmp_file.name, 'rb') as data:
            self.user = {"name":"kamara", "password":"1234", "email":'kd@gmail.com', "passport_photograh":data}
            self.client = APIClient()
            self.response = self.client.post(
                reverse('create'),
                self.user,
                format='multipart')


    def test_model_can_create_a_account(self):

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_user_can_login(self):

        response = self.client.post(
            reverse('login'),
            {'email':self.user['email'], 'password':self.user['password']},
            format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_authenticate_method(self):
        user = User.objects.get(email=self.user['email'], password=self.user['password'])
        authenticate_user = MyAuthBackend()
        response = authenticate_user.authenticate(self.user['email'], self.user['password'])
        self.assertEquals(response, user)



