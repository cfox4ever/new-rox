from django.db import models
from vendors.models import Vendor
from private_storage.fields import PrivateFileField
import os
from datetime import datetime
from simple_history.models import HistoricalRecords
from django.utils.text import slugify
from .fileUtils import get_upload_path , upload_to , BaseFile
from core.models import Branch


class Invoice(models.Model):
   STATUS_CHOICES = [
       ('pending', 'Pending'),
       ('quote', 'Quote'),

       ('requisition', 'Requisition'),
       ('po_received', 'PO Received'),
       ('sent_to_ap', 'Sent to AP'),
       ('completed', 'Completed'),
       ('open_contract', 'Open Contract'),
       ('completed_contract', 'Completed Contract'),
       ('canceled','Canceled'),
       ('on_hold','On Hold')
   ]
   branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_invoices',null=True,blank=True)

   vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
   invoice_number = models.CharField(max_length=100, blank=True, null=True)
   quote_number = models.CharField(max_length=100, blank=True, null=True)
   total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   shipping = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   grand_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   requisition_number = models.CharField(max_length=100, blank=True, null=True)
   po_number = models.CharField(max_length=100, blank=True, null=True)
   status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
   url = models.URLField(blank=True, null=True)
   invoice_date = models.DateTimeField( blank=True, null=True)
   requisition_date = models.DateTimeField(blank=True, null=True)
   po_date = models.DateTimeField(blank=True, null=True)
   received_date = models.DateTimeField( blank=True, null=True)
   sent_to_ap_date = models.DateTimeField( blank=True, null=True)
   created_at = models.DateTimeField( auto_now_add=True, editable=False,blank=True, null=True)
   updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
   history = HistoricalRecords()  # Add history tracking
   def save(self, *args, **kwargs):
       self.grand_total = ((self.total if self.total is not None else 0)
        + (self.shipping if self.shipping is not None else 0)
        +(self.tax if self.tax is not None else 0))
       super().save(*args, **kwargs)
   def __str__(self):
    if self.invoice_number:
        return f"Invoice {self.invoice_number} for {self.vendor.name}"
    else :
        return "No Invoice Number"
    class Meta :
        unique_together = ("invoice_number", "vendor")


class QuoteFile(BaseFile):
   invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE, related_name="quote_files")
   document_type = models.CharField(max_length=50, default="quote")
   number = models.CharField(max_length=100, blank=True, null=True)
   history = HistoricalRecords()
   def __str__(self):
       return f"Quote File - {self.file.name}"
class RequisitionFile(BaseFile):
   invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE, related_name="requisition_files")
   document_type = models.CharField(max_length=50, default="requisition")
   number = models.CharField(max_length=100, blank=True, null=True)
   def __str__(self):
       return f"Requisition File - {self.file.name}"

class InvoiceFile(BaseFile):
   invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE, related_name="invoice_files")
   document_type = models.CharField(max_length=50, default="invoice")
   number = models.CharField(max_length=100, blank=True, null=True)
   history = HistoricalRecords()
   def __str__(self):
       return f"Invoice File - {self.file.name}"
  
class POFile(BaseFile):
   invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE, related_name="po_files")
   document_type = models.CharField(max_length=50, default="po")
   number = models.CharField(max_length=100, blank=True, null=True)
   history = HistoricalRecords()
   def __str__(self):
       return f"PO File - {self.file.name}"
  
class ReceivedFile(BaseFile):
   invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE, related_name="received_files")
   document_type = models.CharField(max_length=50, default="received")
   number = models.CharField(max_length=100, blank=True, null=True)
   history = HistoricalRecords()
  
   def __str__(self):
       return f"Received File - {self.file.name}"
   
class EmailFile(BaseFile):
   invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE, related_name="email_files")
   document_type = models.CharField(max_length=50, default="email")
   number = models.CharField(max_length=100, blank=True, null=True)
   history = HistoricalRecords()
   def __str__(self):
      return f"Email File - {self.file.name}"
class ArchiveFile(BaseFile):
   invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE, related_name="archive_files")
   document_type = models.CharField(max_length=50, default="archive")
   number = models.CharField(max_length=100, blank=True, null=True)
   history = HistoricalRecords()
   def __str__(self):
      return f"Archive File - {self.file.name}"
class Archive(models.Model):
   files = models.ManyToManyField(ArchiveFile, related_name='archives')
   name = models.CharField(max_length=255)
   description = models.TextField(blank=True, null=True)
   history = HistoricalRecords()
class Contract(models.Model):
   name = models.CharField(max_length=255)
   invoices = models.ManyToManyField(Invoice)
   file = PrivateFileField(upload_to='CONTRACT',null=True,blank=True)
   total_invoices_to_date = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
   created_at = models.DateTimeField( auto_now_add=True, editable=False,blank=True, null=True)
   updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
   history = HistoricalRecords()  # Add history tracking
   def save(self, *args, **kwargs):
       self.total_invoices_to_date = sum(invoice.grand_total for invoice in self.invoices.all())
       super().save(*args, **kwargs)
   def __str__(self):
       return self.name
