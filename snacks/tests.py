from datetime import datetime, timezone, timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
import pytz

from snacks.models import Snack
from .serializer import SnackSerializer


class SnacksApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="username", email="email", password="password")
        self.snack = Snack.objects.create(owner=self.user, name="name", description="description")
        self.future_time = datetime.now(timezone.utc) + timedelta(minutes=2)
        self.past_time = datetime.now(timezone.utc) - timedelta(minutes=2)

    def test_snacks_view_permissions(self):
        url = reverse("snack_view")
        # self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.snack)

    # def test_snacks_create_permissions(self):
    #     url = reverse("snack_create")
    #     self.client.login(username=self.user.username, password=self.user.password)
    #     data = {"owner": self.user.pk, "name": "post-name", "description": "post-description"}
    #     response = self.client.post(url, data)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertContains(response, self.snack)

    # def test_snack_?????(self):
    #     url = reverse("snack_detailed", kwargs={"pk": self.snack.pk})
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertContains(response, self.snack)

    # def test_create_snack(self):
    #     url = reverse("snacks_list")
    #     data = {"owner": self.user.pk, "name": "post-name", "description": "post-description"}
    #     response = self.client.post(url, data, format='json')
    #     actual_time = datetime.strptime(response.data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
    #         tzinfo=pytz.UTC)
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(len(Snack.objects.all()),2)
    #     self.assertEqual(User.objects.get(pk=response.data["owner"]), self.user)
    #     self.assertEqual(response.data['name'], 'post-name')
    #     self.assertEqual(response.data['description'], 'post-description')
    #     self.assertGreater(actual_time, self.past_time)
    #     self.assertLess(actual_time, self.future_time)
    #
    # def test_update_snack(self):
    #     url = reverse("snack_detailed", kwargs={"pk": self.snack.pk})
    #     data = {'owner': self.user.pk, 'name': "updated-name", 'description': "description"}
    #     response = self.client.put(url, data, format='json')
    #     actual_time = datetime.strptime(response.data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
    #         tzinfo=pytz.UTC)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(Snack.objects.all()),1)
    #     self.assertEqual(User.objects.get(pk=response.data["owner"]), self.user)
    #     self.assertEqual(response.data['name'], 'updated-name')
    #     self.assertEqual(response.data['description'], 'description')
    #     self.assertGreater(actual_time, self.past_time)
    #     self.assertLess(actual_time, self.future_time)
    #
    # def test_delete_snack(self):
    #     url = reverse("snack_detailed", kwargs={"pk": self.snack.pk})
    #     response = self.client.delete(url, follow=True)
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(len(Snack.objects.all()),0)


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