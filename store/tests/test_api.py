from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksTestCase(APITestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(
            name="Test Book 1", price=25, author_name="Author 1"
        )
        self.book_2 = Book.objects.create(
            name="Test Book 2 from Author 2", price=55, author_name="Author 1"
        )
        self.book_3 = Book.objects.create(
            name="Test Book 3", price=60, author_name="Author 2"
        )

    def test_get(self):
        # Request to server via router name from "url.py".
        url = reverse("book-list")
        response = self.client.get(url)

        # Getting data from serializer.
        serializer_data = BooksSerializer(
            [self.book_1, self.book_2, self.book_3], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        # Request to server via router name from "url.py".
        url = reverse("book-list")
        response = self.client.get(url, data={"search": "Author 2"})

        # Getting data from serializer.
        serializer_data = BooksSerializer([self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_order_1(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"ordering": "author_name"})

        serializer_data = BooksSerializer(
            [self.book_1, self.book_2, self.book_3], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_order_2(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"ordering": "-author_name"})

        serializer_data_1 = BooksSerializer(
            [self.book_3, self.book_2, self.book_1], many=True
        ).data
        serializer_data_2 = BooksSerializer(
            [self.book_3, self.book_1, self.book_2], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn(response.data, [serializer_data_1, serializer_data_2])

    def test_get_order_3(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"ordering": "price"})

        serializer_data = BooksSerializer(
            [self.book_1, self.book_2, self.book_3], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_order_4(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"ordering": "-price"})

        serializer_data = BooksSerializer(
            [self.book_3, self.book_2, self.book_1], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
