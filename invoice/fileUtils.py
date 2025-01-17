from django.db import models
from private_storage.fields import PrivateFileField
import os
from django.contrib.auth.models import User
from django.utils.timezone import now


# Function to dynamically generate file paths
def get_upload_path(instance, filename):
    """
    Generate a custom file path:
    QUOTE-VENDOR NAME-<document_type>-<number>.<extension>
    """
    base_name, extension = os.path.splitext(filename)

    # Determine the vendor name based on the instance type
    if hasattr(instance, "invoice") and instance.invoice and instance.invoice.vendor:
        vendor_name = instance.invoice.vendor.name
    elif (
        hasattr(instance, "contract") and instance.contract and instance.contract.vendor
    ):
        vendor_name = instance.contract.vendor.name
    else:
        vendor_name = "UNKNOWN"

    # Retrieve relevant data from the instance
    document_type = instance.document_type or "file"  # E.g., quote, invoice, etc.
    # number = instance.number or "0000"  # Invoice number, PO number, etc.
    if document_type == 'contract' :
        number = instance.invoice.contract_number or "CONT000"  
    elif document_type == 'invoice' :
        number = instance.invoice_number or "INV000"  
    elif document_type == 'quote' :
        number = instance.invoice.quote_number or "Q000"  
    elif document_type == 'requisition' :
        number = instance.invoice.requisition_number or "REQ000"  
    elif document_type == 'po' :
        number = instance.invoice.po_number or "PO000"  
    elif document_type == 'received' :
        number = instance.invoice.invoice_number or "REC000"  
    elif document_type == 'email' :
        number = instance.invoice.invoice_number or "EM000"  
    elif document_type == 'archive' :
        number = instance.invoice.invoice_number or "AR000"  
    else:
         number = "000"    
    # Create a sanitized filename
    clean_vendor_name = vendor_name.replace(" ", "_").upper()
    clean_document_type = document_type.upper()
    new_filename = f"{clean_document_type}-{clean_vendor_name}-{number}{extension}"

    current_time = now()
    year = current_time.year
    month = current_time.month

    return os.path.join(
        f"uploads/{clean_document_type}/{clean_vendor_name}/{year}/{month}",
        new_filename,
    )


# Base abstract model for file-related models
class BaseFile(models.Model):
    file = PrivateFileField(upload_to=get_upload_path)
    created_by = created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

    # Delete the old file if it exists and a new file is being uploaded
    def save(self, *args, **kwargs):
        if self.pk:
            old_file = FileBase.objects.filter(pk=self.pk).first()
            if old_file and old_file.file != self.file:
                old_file.file.delete(save=False)
        super().save(*args, **kwargs)

    # Delete the file when the model instance is deleted
    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)