from django.db import models
from vendors.models import Vendor
from private_storage.fields import PrivateFileField
import os
from datetime import datetime
from simple_history.models import HistoricalRecords
from django.utils.text import slugify
from .fileUtils import get_upload_path  , BaseFile
from core.models import Branch
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

CONTRACT_CHOICES = [
         ('pending', 'Pending'),
         ('quote', 'Quote'),
    
         ('requisition', 'Requisition'),
         ('po', 'PO'),
         ('pending_po', 'Pending PO'),
         ('sent_to_vendor', 'Sent to Vendor'),
         
        
         ('completed', 'Completed'),
         
         
      
         ('on_hold','On Hold'),
         ('cancelled','Cancelled')
    ]
STATUS_CHOICES = [
       ('pending', 'Pending'),
       ('quote', 'Quote'),

       ('requisition', 'Requisition'),
       ('po_received', 'Received'),
       ('sent_to_ap', 'Sent to AP'),
       ('completed', 'Completed'),
       ('contract_invoice','Contract Invoice'),
       
     
       ('on_hold','On Hold'),
       ('cancelled','Cancelled'),
        ('rejected','Rejected'),
        ('unknown','Unknown'),

   ]
class ContractFile(BaseFile):
   contract = models.ForeignKey("Contract", on_delete=models.CASCADE, related_name="contract_files")
   document_type = models.CharField(max_length=50, default="contract")
   number = models.CharField(max_length=100, blank=True, null=True)
   history = HistoricalRecords()
   def __str__(self):
       return f"Contract File - {self.file.name}"

class Contract(models.Model):
   branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_contracts',null=True,blank=True)
   vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,blank=True, null=True)
   contract_number = models.CharField(max_length=100, blank=True, null=True)
   quote_number = models.CharField(max_length=100, blank=True, null=True)
   requisition_number = models.CharField(max_length=100, blank=True, null=True)
   po_number = models.CharField(max_length=100, blank=True, null=True)
   status = models.CharField(max_length=20, choices=CONTRACT_CHOICES, default='pending')
   url = models.URLField(blank=True, null=True)
   total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   grand_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   invoices_count = models.IntegerField(default=0)
   contract_start_date = models.DateTimeField( blank=True, null=True)
   contract_end_date = models.DateTimeField( blank=True, null=True)
   po_date = models.DateTimeField(blank=True, null=True)
   requisition_date = models.DateTimeField(blank=True, null=True)
   quote_date = models.DateTimeField(blank=True, null=True)
   send_to_vendor =models.BooleanField(default=True)
   send_to_vendor_date = models.DateTimeField( blank=True, null=True)
   total_invoices_to_date = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
   notes= models.TextField(max_length=2000 ,blank=True, null=True)

   created_at = models.DateTimeField( auto_now_add=True, editable=False,blank=True, null=True)
   updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
   favorited_by = models.ManyToManyField(
       User, related_name="favorite_contracts", blank=True
   )
   created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,
        related_name="contracts")
   history = HistoricalRecords()  # Add history tracking
#    def save(self, *args, **kwargs):
#     # Aggregate the sum of grand_total from related invoices
#        self.total_invoices_to_date = (
#            self.contract_invoices.aggregate(total=Sum('grand_total'))['total'] or 0
#        )
#        super().save(*args, **kwargs)
   def __str__(self):
       return f"Contract {self.contract_number or 'N/A'}"
# @receiver(post_save, sender=Contract)
# def update_total_invoices_to_date(sender, instance, **kwargs):
# # Calculate the sum of grand_total from related invoices
#    instance.total_invoices_to_date = (
#        instance.contract_invoices.aggregate(total=Sum('grand_total'))['total'] or 0
#    )
# Save the updated total back to the contract
#    instance.save(update_fields=['total_invoices_to_date'])


class Invoice(models.Model):
   
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
   send_to_vendor =models.BooleanField(default=True)
   send_to_vendor_date = models.DateTimeField( blank=True, null=True)
   created_at = models.DateTimeField( auto_now_add=True, editable=False,blank=True, null=True)
   updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
   favorited_by = models.ManyToManyField(
       User, related_name="favorite_invoices", blank=True
   )
   notes= models.TextField(max_length=2000 ,blank=True, null=True)
   contract = models.ForeignKey(Contract,on_delete=models.SET_NULL,null=True,blank=True,related_name='contract_invoices')
   created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,
        related_name="invoices")
   history = HistoricalRecords()  # Add history tracking
   class Meta:
        ordering =['-id']


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
class ArchiveFile(models.Model):
   invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE, related_name="archive_files")
   document_type = models.CharField(max_length=50, default="archive")
   number = models.CharField(max_length=100, blank=True, null=True)
   file = PrivateFileField(upload_to=get_upload_path)
   created_by = created_by = models.ForeignKey(
       User,
       on_delete=models.SET_NULL,
       null=True,
       blank=True,
       
   ) 
   created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
   updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
   history = HistoricalRecords()
   def __str__(self):
      return f"Archive File - {self.file.name}"
   
       
# Delete the old file if it exists and a new file is being uploaded
   def save(self, *args, **kwargs):
       """
       Before saving a new archive file, delete all old archive records and files for the same invoice.
       """
       # If this is a new instance (not an update)
       if not self.pk:
           # Delete all existing records for the same invoice
           old_files = ArchiveFile.objects.filter(invoice=self.invoice)
           for old_file in old_files:
               old_file.delete()
       super().save(*args, **kwargs)
# Delete the file when the model instance is deleted
   def delete(self, *args, **kwargs):
       self.file.delete(save=False)
       super().delete(*args, **kwargs)



class Archive(models.Model):
   
   files = models.ManyToManyField(ArchiveFile, related_name='archives')
   name = models.CharField(max_length=255)
   description = models.TextField(blank=True, null=True)
   history = HistoricalRecords()
   
   
   

