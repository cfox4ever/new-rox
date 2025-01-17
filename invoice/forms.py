from django import forms
from .models import (
    Invoice,
    QuoteFile,
    RequisitionFile,
    InvoiceFile,
    POFile,
    ReceivedFile,
    EmailFile,
    ArchiveFile,
    Archive,
    Contract,
    ContractFile,
)
from django.core.exceptions import ValidationError


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
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
            "notes": forms.Textarea(
                attrs={
                    "rows": "5",
                    "cols": "4,",
                    # "readonly": True,
                }
            ),
        }


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # Enable multiple file selection


class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def clean(self, value, initial=None):
        if not value:
            raise ValidationError("No files were uploaded.")
        if not isinstance(value, list):
            value = [value]
        return value


class MultiFileUploadForm(forms.Form):

    files = MultiFileField()

    def clean(self):
        cleaned_data = super().clean()
        files = cleaned_data.get("files")
        if not files:
            raise ValidationError("No files uploaded.")
        return cleaned_data


class ContractForm(forms.ModelForm):
    # contract = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Contract
        fields = "__all__"
        widgets = {
            "contract_start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    # "readonly": True,
                }
            ),
            "contract_end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    # "readonly": True,
                }
            ),
            "po_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    # "readonly": True,
                }
            ),
            "requisition_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    # "readonly": True,
                }
            ),
            "quote_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    # "readonly": True,
                }
            ),
            "send_to_vendor_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    # "readonly": True,
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": "5",
                    "cols": "2,",
                    # "readonly": True,
                }
            ),
            "contract": forms.HiddenInput(),
          
        }
        