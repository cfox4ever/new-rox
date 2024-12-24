from django import forms
from .models import (Invoice,QuoteFile,RequisitionFile,InvoiceFile,POFile,
ReceivedFile,EmailFile,ArchiveFile,Archive,Contract)


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields="__all__"
        widgets = {
            "sent_to_ap_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "Recieved Date",
                }
            ), 
            "requisition_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "Recieved Date",
                }
            ), 
            "po_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "Recieved Date",
                }
            ), 
            "invoice_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "Recieved Date",
                }
            ), 
            "received_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "Recieved Date",
                }
            ), 
            "grand_total": forms.DateInput(
                attrs={
                    "class": "form-control",
                    # "readonly": True,
                    
                }
            ), 
        }