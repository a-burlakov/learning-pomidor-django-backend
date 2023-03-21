from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.CharField("Название", max_length=255)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    author_name = models.CharField("Автор", max_length=255)
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        on_delete=models.SET_NULL,
        null=True,
        related_name="my_books",
    )
    readers = models.ManyToManyField(
        User, through="UserBookRelation", related_name="books"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.name} by {self.author_name} ({self.price} rub.)"

    # def save(self):
    #     pass

    # def get_absolute_url(self):
    #     pass


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, "Ok"),
        (2, "Fine"),
        (3, "Good"),
        (4, "Amazing"),
        (5, "Incredible"),
    )

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True
    )
    book = models.ForeignKey(
        Book, verbose_name="Книга", on_delete=models.CASCADE, null=True
    )
    like = models.BooleanField("Лайк", default=False)
    in_bookmarks = models.BooleanField("В закладках", default=False)
    rate = models.PositiveSmallIntegerField("Оценка", choices=RATE_CHOICES)

    class Meta:
        verbose_name = "Отношение книги и пользователя"
        verbose_name_plural = "Отношения книг и пользователей"

    def __str__(self):
        return f"{self.user.username}: {self.book.name}, ({self.rate})"
