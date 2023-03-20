from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(
            name="Test Book 1", price=25, author_name="Test Author"
        )
        book_2 = Book.objects.create(
            name="Test Book 2", price=52, author_name="Test Author"
        )
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                "id": book_1.id,
                "name": "Test Book 1",
                "price": "25.00",
                "author_name": "Test Author",
                "owner": None,
            },
            {
                "id": book_2.id,
                "name": "Test Book 2",
                "price": "52.00",
                "author_name": "Test Author",
                "owner": None,
            },
        ]
        self.assertEqual(expected_data, data)
