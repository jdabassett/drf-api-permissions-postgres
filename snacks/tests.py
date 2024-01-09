from datetime import datetime, timezone, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
import pytz

from snacks.models import Snack
from .serializer import SnackSerializer


class SnacksApiTests(APITestCase):

    def setUp(self):
        self.future_time = datetime.now(timezone.utc) + timedelta(minutes=2)
        self.past_time = datetime.now(timezone.utc) - timedelta(minutes=2)
        self.user = get_user_model().objects.create_user(username="username", password="password")
        self.snack = Snack.objects.create(name="apples", owner=self.user, description="A type of fruit.")
        self.client.login(username="username", password="password")

    def test_snack_model(self):
        snack = Snack.objects.get(id=1)
        actual_owner = str(snack.owner)
        actual_name = str(snack.name)
        actual_description = str(snack.description)
        self.assertEqual(actual_owner, str(self.snack.owner))
        self.assertEqual(actual_name, self.snack.name)
        self.assertEqual(actual_description, self.snack.description)

    def test_snack_view_get(self):
        url = reverse('snack_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        snacks = response.data
        self.assertEqual(len(snacks), 1)
        self.assertContains(response, self.snack)

    def test_snack_create_get(self):
        url = reverse('snack_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        snacks = response.data
        self.assertEqual(len(snacks), 1)
        self.assertContains(response, self.snack)

    def test_snack_create_post(self):
        url = reverse('snack_create')
        data = {"owner": self.user.pk, "name": "post-name", "description": "post-description"}
        response = self.client.post(url, data, format='json')
        actual_time = datetime.strptime(response.data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
            tzinfo=pytz.UTC)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Snack.objects.all()),2)
        self.assertEqual(User.objects.get(pk=response.data["owner"]), self.user)
        self.assertEqual(response.data['name'], 'post-name')
        self.assertEqual(response.data['description'], 'post-description')
        self.assertGreater(actual_time, self.past_time)
        self.assertLess(actual_time, self.future_time)

    def test_snack_update_get(self):
        url = reverse('snack_update', kwargs={'pk': self.snack.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_snack_update_put(self):
        data = {"owner": self.user.pk, "name": "put-name", "description": "put-description"}
        url = reverse('snack_update', kwargs={'pk': self.snack.pk})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        actual_time = datetime.strptime(response.data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
            tzinfo=pytz.UTC)
        self.assertEqual(User.objects.get(pk=response.data["owner"]), self.user)
        self.assertEqual(response.data['name'], 'put-name')
        self.assertEqual(response.data['description'], 'put-description')
        self.assertGreater(actual_time, self.past_time)
        self.assertLess(actual_time, self.future_time)

    def test_snack_update_delete(self):
        url = reverse('snack_update', kwargs={'pk': self.snack.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_snack_create_fail(self):
        self.client.logout()
        url = reverse('snack_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_snack_update_fail(self):
        self.client.logout()
        url = reverse('snack_update', kwargs={'pk': self.snack.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SnacksSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="username", email="email", password="password")
        self.snack_valid = {'owner': self.user.id, 'name': 'name', 'description': 'description'}
        self.snack_invalid = {'owner': None , 'name': 'name', 'description': 'description'}

    def test_snack_serializer_valid(self):
        actual = SnackSerializer(data=self.snack_valid)
        self.assertTrue(actual.is_valid())
        self.assertEqual(actual.errors, {})

    def test_snack_serializer_invalid(self):
        actual = SnackSerializer(data=self.snack_invalid)
        self.assertFalse(actual.is_valid())
        self.assertTrue("owner" in actual.errors)