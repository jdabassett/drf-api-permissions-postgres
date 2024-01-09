from datetime import datetime, timezone, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import SnackCollection
from snacks.models import Snack


class SnacksApiTests(APITestCase):

    def setUp(self):
        self.future_time = datetime.now(timezone.utc) + timedelta(minutes=2)
        self.past_time = datetime.now(timezone.utc) - timedelta(minutes=2)
        self.user = get_user_model().objects.create_user(username="username", password="password")
        self.snack1 = Snack.objects.create(name="1", owner=self.user, description="1")
        self.snack2 = Snack.objects.create(name="2", owner=self.user, description="2")
        self.snack3 = Snack.objects.create(name="3", owner=self.user, description="3")
        self.snack_collection = SnackCollection.objects.create(owner=self.user)
        self.snack_collection.snacks.add(self.snack1, self.snack2)
        self.client.login(username="username", password="password")

    def test_snack_model(self):
        snack_collection = SnackCollection.objects.get(id=self.snack_collection.id)
        actual_owner = str(snack_collection.owner)
        self.assertEqual(actual_owner, str(self.user))

    def test_snack_collection_view_get(self):
        url = reverse('snack_collection_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(SnackCollection.objects.all()), 1)

    def test_snack_collection_create_get(self):
        url = reverse('snack_collection_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_snack_collection_create_post(self):
        url = reverse('snack_collection_create')
        data = {"owner": self.user.pk, "snacks": [self.snack1.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(SnackCollection.objects.all()), 2)
        self.assertEqual(User.objects.get(pk=response.data["owner"]), self.user)
        self.assertEqual(response.data['snacks'][0], self.snack1.id)

    def test_snack_collection_update_get(self):
        url = reverse('snack_collection_update', kwargs={'pk': self.snack_collection.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_snack_update_put(self):
        data = {"owner": self.user.pk, "snacks": [self.snack2.pk,self.snack3.pk]}
        url = reverse('snack_collection_update', kwargs={'pk': self.snack_collection.pk})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(User.objects.get(pk=response.data["owner"]), self.user)
        self.assertEqual(sorted(response.data['snacks']), [self.snack2.pk,self.snack3.pk])

    def test_snack_collection_update_delete(self):
        url = reverse('snack_collection_update', kwargs={'pk': self.snack_collection.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_snack_collection_create_fail(self):
        self.client.logout()
        url = reverse('snack_collection_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_snack_collection_update_fail(self):
        self.client.logout()
        url = reverse('snack_collection_update', kwargs={'pk': self.snack_collection.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
