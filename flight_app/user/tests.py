from django.test import TestCase

# Create your tests here.
from flight_app.user.models import User,UserManager
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
import json
from PIL import Image
import tempfile
from flight_app.user.backends import MyAuthBackend


class ModelTestCase(TestCase):
    def setUp(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        with open(tmp_file.name, 'rb') as data:
            self.user = {"name":"kamara", "password":"1@thyktt", "email":'kd@gmail.com', "passport_photograh":data}
            self.client = APIClient()
            self.response = self.client.post(
                reverse('create'),
                self.user,
                format='multipart')



    def test_model_can_create_a_account(self):

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


    def test_model_cant_create_a_account_with_short_password(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        with open(tmp_file.name, 'rb') as data:
            user = {"name":"kamara", "password":"1thyktt", "email":'ukd@gmail.com', "passport_photograh":data}
            client = APIClient()
            response = client.post(
                reverse('create'),
                user,
                format='multipart')
        self.assertEqual(response.data, {'Message':'The password should contain atleast a special character,number and should be 8-12 characters'})


    def test_model_cant_create_a_account_with_existing_email(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        with open(tmp_file.name, 'rb') as data:
            user = {"name":"kamara", "password":"1thyktt", "email":'kd@gmail.com', "passport_photograh":data}
            client = APIClient()
            response = client.post(
                reverse('create'),
                user,
                format='multipart')
        self.assertEqual(response.data, {'Message':'Wrong format/Email already exists'})

    def test_model_cant_create_an_account_with_invalid_image(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpeg')
        image.save(tmp_file)
        with open(tmp_file.name, 'rb') as data:
            user = {"name":"kamara", "password":"1t@frhyktt", "email":'ukdf@gmail.com', "passport_photograh":data}
            client = APIClient()
            response = client.post(
                reverse('create'),
                user,
                format='multipart')
        self.assertEqual(response.data, {'Message':'Invalid image type.Only .jpg and .png images allowed!'})


    def test_model_cant_create_an_account_without_image(self):
        user = {"name":"kamara", "password":"1t@frhyktt", "email":'ukdf@gmail.com', "passport_photograh":''}
        client = APIClient()
        response = client.post(
            reverse('create'),
            user,
            format='multipart')
        self.assertEqual(response.data, {'Message':'Profile picture is required'})



    def test_user_can_login(self):

        response = self.client.post(
            reverse('login'),
            {'email':self.user['email'], 'password':self.user['password']},
            format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)


    def test_user_cant_login(self):

        response = self.client.post(
            reverse('login'),
            {'email':'iigmail.com', 'password':self.user['password']},
            format='json')
        self.assertEquals(response.data, {'Message': 'Invalid credientals'})

    def test_user_change_image(self):
        response = self.client.post(
            reverse('login'),
            {'email':self.user['email'], 'password':self.user['password']},
            format='json')
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        client = APIClient()
        response = self.client.post(
            reverse('login'),
            {'email':self.user['email'], 'password':self.user['password']},
            format='json')
        client.credentials(HTTP_AUTHORIZATION=response.data['token'])
        with open(tmp_file.name, 'rb') as data:
            res = client.put(
                reverse('create'),
                {"passport_photograh":data},
                format='multipart')
            self.assertEquals(res.data, {'Message': 'Image successfully changed'})


    def test_user_delete_image(self):
        client = APIClient()
        response = self.client.post(
            reverse('login'),
            {'email':self.user['email'], 'password':self.user['password']},
            format='json')
        client.credentials(HTTP_AUTHORIZATION=response.data['token'])
        res = client.delete(
                reverse('create'),
                format='json')
        self.assertEquals(res.data, {'Message': 'Image successfully removed'})

    def test_user_change_image_without_token(self):

        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='')
        with open(tmp_file.name, 'rb') as data:
            res = client.put(
                reverse('create'),
                {"passport_photograh":data},
                format='multipart')
            self.assertEquals(res.data, {'Message': 'Missing token key'})

    def test_authenticate_method(self):
        user = User.objects.filter(email=self.user['email'], password=self.user['password']).first()
        authenticate_user = MyAuthBackend()
        response = authenticate_user.authenticate(self.user['email'], self.user['password'])
        invalid_response = authenticate_user.authenticate(self.user['email'], '89')
        self.assertEquals(response, user)
        self.assertEquals(invalid_response, None)


    def test_user_manager(self):
        new_user = User.objects.create_user("nana@email.com",self.user['name'],self.user['password'])
        staffuser = User.objects.create_staffuser("short@email.com", self.user['name'], self.user['password'])
        supperuser = User.objects.create_superuser("short3@email.com", self.user['name'], self.user['password'])
        self.assertEquals(new_user.__str__(),new_user.email)
        self.assertEquals("nana@email.com", new_user.email)
        self.assertEquals("short@email.com", staffuser.email)
        self.assertEquals("short3@email.com", supperuser.email)







