from django.contrib import admin

from .models import (Invoice,QuoteFile,RequisitionFile,InvoiceFile,POFile,ReceivedFile,
EmailFile,ArchiveFile,Archive,Contract)
admin.site.register(Invoice)