from django.conf import settings
from django.db import models


class Loan(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'requested', 'Requested'
        BORROWED = 'borrowed', 'Borrowed'
        RETURNED = 'returned', 'Returned'
        REJECTED = 'rejected', 'Rejected'

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='loans',
    )
    book = models.ForeignKey(
        'library.Book',
        on_delete=models.PROTECT,
        related_name='loans',
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.REQUESTED,
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    borrowed_at = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    returned_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.member} - {self.book}'


class ExtensionRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name='extension_requests',
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Extension for {self.loan}'


class Fine(models.Model):
    loan = models.OneToOneField(
        Loan,
        on_delete=models.CASCADE,
        related_name='fine',
    )
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Fine {self.amount} for {self.loan}'