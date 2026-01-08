import uuid
from django.db import models



# Create your models here.
class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    google_place_id = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255)

    address = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    raw_payload = models.JSONField()  # Full Google response snapshot

    created_at = models.DateTimeField(auto_now_add=True)
