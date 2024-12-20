from django.db import models
from .setups import STATES
from simple_history.models import HistoricalRecords

class Branch(models.Model):
    name = models.CharField(max_length=250, null=True, unique=True)
    phone = models.CharField(
        max_length=20, blank=True, help_text="Contact phone number", null=True
    )
    address_1 = models.CharField(max_length=128, null=True)
    address_2 = models.CharField(max_length=128, blank=True, null=True)

    city = models.CharField(max_length=64, null=True)
    state = models.CharField(choices=STATES, max_length=2, null=True)
    zip_code = models.CharField(max_length=50, null=True)

    dateCreated = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    status = models.BooleanField()
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
