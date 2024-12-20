from django.db import models
from private_storage.fields import PrivateFileField


# Function to dynamically generate file paths
def get_upload_path(instance, filename):
   """
   Generate a custom file path:
   QUOTE-VENDOR NAME-<document_type>-<number>.<extension>
   """
   base_name, extension = os.path.splitext(filename)
   # Retrieve relevant data from the instance
   vendor_name = instance.invoice.vendor.name if instance.invoice and instance.invoice.vendor else "UNKNOWN"
   document_type = instance.document_type or "file"  # E.g., quote, invoice, etc.
   number = instance.number or "0000"  # Invoice number, PO number, etc.
   # Create a sanitized filename
   clean_vendor_name = vendor_name.replace(" ", "_").upper()
   clean_document_type = document_type.upper()
   new_filename = f"QUOTE-{clean_vendor_name}-{clean_document_type}-{number}{extension}"
   return os.path.join("uploads", new_filename)


def upload_to(instance, filename, file_type):
   ext = filename.split('.')[-1]
   vendor_name = slugify(instance.invoice.vendor.name)
   quote_number = getattr(instance.invoice, 'quote_number', 'unknown')
   filename = f"{file_type.upper()}_{quote_number}_{vendor_name}.{ext}"
   year = instance.invoice.invoice_date.year
   return os.path.join(f"uploads/{file_type.lower()}/{year}/", filename)


# Base abstract model for file-related models
class BaseFile(models.Model):
   file = models.FileField(upload_to=get_upload_path)
   created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
   updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
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