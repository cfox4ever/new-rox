from django.db import models
from private_storage.fields import PrivateFileField
from simple_history.models import HistoricalRecords
from core.models import Branch
from  invoice.fileUtils import get_upload_path , upload_to , BaseFile
from django.dispatch import receiver
from django.db.models.signals import post_delete


STATUS_CHOICES = [
       ('pending', 'Pending'),
       ('on_hold','On Hold'),
       ('active', 'Active'),

       ('in-active', 'In-Active'),
       
   ]
class Vendor(models.Model):
   branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_vendors',null=True,blank=True)
   name = models.CharField(max_length=255)
   phone = models.CharField(max_length=20)
   email = models.EmailField()
   services = models.TextField()
   notes = models.TextField(blank=True, null=True)
   status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
   created_at = models.DateTimeField( auto_now_add=True, editable=False,blank=True, null=True)
   updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
   history = HistoricalRecords()  # Add history tracking
   def __str__(self):
       return self.name

   class Meta:
        ordering = ["name"]
class File(models.Model):
   vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,blank=True, null=True,related_name='vendor_files') 
   file=PrivateFileField(upload_to='vendors/')
   def __str__(self):
       return f"Vendor File - {self.file.name}"

@receiver(post_delete, sender=File)
def delete_file_on_record_delete(sender, instance, **kwargs):
   if instance.file:
       instance.file.delete(False)