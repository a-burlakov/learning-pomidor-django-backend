from django.db import models


class Book(models.Model):
    name = models.CharField("Название", max_length=255)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        pass

    def save(self):
        pass

    def get_absolute_url(self):
        pass
