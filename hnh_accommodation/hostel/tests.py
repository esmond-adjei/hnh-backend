from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Hostel


class HostelTests(APITestCase):
    def setUp(self):
        # Create a test hostel
        self.hostel_data = {
            'name': 'Test Hostel',
            'location': 'Test Location',
            'available_rooms': 10,
            'description': 'Test Description',
            'rating': 4.5,
        }
        self.hostel = Hostel.objects.create(**self.hostel_data)

        # urls endpoints
        self.list_url = reverse('hostel-list')
        self.create_url = reverse('create-hostel')
        self.update_url = reverse('update-hostel', args=[self.hostel.id])

    def test_hostel_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print(response.data)
        self.assertEqual(len(response.data), 1)
        # ... add assertions for other fields

    def test_hostel_detail(self):
        detail_url = reverse('hostel-detail', args=[self.hostel.id])

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.hostel_data['name'])
        self.assertEqual(response.data['location'],
                         self.hostel_data['location'])
        # ... add assertions for other fields

    def test_create_hostel(self):
        response = self.client.post(
            self.create_url, self.hostel_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.hostel_data['name'])
        self.assertEqual(response.data['location'],
                         self.hostel_data['location'])
        # ... add assertions for other fields

    def test_update_hostel(self):
        update_data = {
            'name': 'Updated Hostel',
            'rating': 4.8,
        }

        response = self.client.put(self.update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_hostel = Hostel.objects.get(id=self.hostel.id)

        self.assertEqual(updated_hostel.name, update_data['name'])
        self.assertEqual(updated_hostel.rating, update_data['rating'])
        # ... add assertions for other fields

    def test_delete_hostel(self):
        delete_url = reverse('delete-hostel', args=[self.hostel.id])

        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Hostel.objects.filter(id=self.hostel.id).exists())
