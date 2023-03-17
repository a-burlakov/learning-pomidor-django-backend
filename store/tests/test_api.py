from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksTestCase(APITestCase):
    def test_get(self):
        # Creating test data.
        book_1 = Book.objects.create(name="Test Book 1", price=25)
        book_2 = Book.objects.create(name="Test Book 2", price=52)

        # Request to server via router name from "url.py".
        url = reverse("book-list")
        response = self.client.get(url)

        # Getting data from serializer.
        serializer_data = BooksSerializer([book_1, book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
