import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testusername")
        self.book_1 = Book.objects.create(
            name="Test Book 1", price=25, author_name="Author 1", owner=self.user
        )
        self.book_2 = Book.objects.create(
            name="Test Book 2 from Author 2",
            price=55,
            author_name="Author 1",
            owner=self.user,
        )
        self.book_3 = Book.objects.create(
            name="Test Book 3", price=60, author_name="Author 2", owner=self.user
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

    def test_get_detail(self):
        # Request to server via router name from "url.py".
        url = reverse("book-detail", args=(self.book_1.id,))
        response = self.client.get(url)

        # Getting data from serializer.
        serializer_data = BooksSerializer(self.book_1).data
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

    def test_create(self):
        self.assertEqual(Book.objects.all().count(), 3)
        url = reverse("book-list")
        data = {
            "name": "Programming in Python 3",
            "price": 150,
            "author_name": "Mark Summerfield",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)

        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Book.objects.all().count(), 4)
        self.assertEqual(Book.objects.last().owner, self.user)

    def test_update(self):
        self.assertEqual(Book.objects.all().count(), 3)
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 777,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)

        response = self.client.put(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Book.objects.all().count(), 3)

        self.book_1.refresh_from_db()
        self.assertEqual(777, self.book_1.price)

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username="test_username2")
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 777,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)

        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(
            response.data,
            {
                "detail": ErrorDetail(
                    string="You do not have permission to perform this action.",
                    code="permission_denied",
                )
            },
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Book.objects.all().count(), 3)

        self.book_1.refresh_from_db()
        self.assertEqual(25, self.book_1.price)

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username="test_username2", is_staff=True)
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 777,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)

        response = self.client.put(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Book.objects.all().count(), 3)

        self.book_1.refresh_from_db()
        self.assertEqual(777, self.book_1.price)

    def test_delete(self):
        self.assertEqual(Book.objects.all().count(), 3)
        url = reverse("book-detail", args=(self.book_1.id,))

        self.client.force_login(self.user)

        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Book.objects.all().count(), 2)
