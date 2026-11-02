from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    publication_year = models.PositiveSmallIntegerField()
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name='books',
    )
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    @property
    def is_available(self):
        return self.available_copies > 0

    def __str__(self):
        return self.title