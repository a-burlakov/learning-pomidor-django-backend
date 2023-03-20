from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.CharField("Название", max_length=255)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    author_name = models.CharField("Автор", max_length=255)
    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.SET_NULL, null=True
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
