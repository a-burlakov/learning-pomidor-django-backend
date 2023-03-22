from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(
            name="Test Book 1", price=25, author_name="Test Author"
        )
        book_2 = Book.objects.create(
            name="Test Book 2", price=52, author_name="Test Author"
        )
        user_1 = User.objects.create(username="user1")
        user_2 = User.objects.create(username="user2")
        user_3 = User.objects.create(username="user3")

        UserBookRelation.objects.create(user=user_1, book=book_1, like=True)
        UserBookRelation.objects.create(user=user_2, book=book_1, like=True)
        UserBookRelation.objects.create(user=user_3, book=book_2, like=True)

        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                "id": book_1.id,
                "name": "Test Book 1",
                "price": "25.00",
                "author_name": "Test Author",
                "likes_count": 2,
            },
            {
                "id": book_2.id,
                "name": "Test Book 2",
                "price": "52.00",
                "author_name": "Test Author",
                "likes_count": 1,
            },
        ]
        self.assertEqual(expected_data, data)
