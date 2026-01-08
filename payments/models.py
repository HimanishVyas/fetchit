from django.db import models
import uuid

# Create your models here.


class Payment(models.Model):

    class Method(models.TextChoices):
        COD = "COD"
        UPI = "UPI"

    class Status(models.TextChoices):
        PENDING = "PENDING"
        PAID = "PAID"
        FAILED = "FAILED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="payment"
    )

    method = models.CharField(max_length=10, choices=Method.choices)
    status = models.CharField(max_length=10, choices=Status.choices)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)



class RunnerPayout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    runner = models.ForeignKey(
        "accounts.Runner",
        on_delete=models.CASCADE,
        related_name="payouts"
    )
    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="runner_payout"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
