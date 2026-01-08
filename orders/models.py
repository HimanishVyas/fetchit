
from django.db import models
import uuid


# ------importing other models------
from accounts.models import (
    User, 
    Runner
    )
from places.models import Place
# Create your models here.


class Order(models.Model):

    class Status(models.TextChoices):
        CREATED = "CREATED"
        RUNNER_ASSIGNED = "RUNNER_ASSIGNED"
        AWAITING_USER_APPROVAL = "AWAITING_USER_APPROVAL"
        PURCHASED = "PURCHASED"
        DELIVERED = "DELIVERED"
        CANCELLED_PRE_VISIT = "CANCELLED_PRE_VISIT"
        CANCELLED_POST_VISIT = "CANCELLED_POST_VISIT"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    runner = models.ForeignKey(
        "accounts.Runner",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    place = models.ForeignKey("places.Place", on_delete=models.PROTECT)

    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.CREATED,
        db_index=True
    )

    # delivery snapshot
    delivery_lat = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_lng = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_address = models.TextField()

    # 🔑 PRICING (TOTAL ONLY)
    quoted_total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    effort_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    approval_deadline_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ItemRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


class OrderEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="events"
    )

    status = models.CharField(max_length=32)
    meta = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
