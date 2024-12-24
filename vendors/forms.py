from django import forms
from .models import Vendor,File
from django.forms.widgets import ClearableFileInput
from django.core.exceptions import ValidationError

class VendorForm(forms.ModelForm):
   
   class Meta:
       model = Vendor
       fields = ['branch','name', 'phone', 'email', 'services', 'notes','status']
    #    widgets = {
    #        'services': forms.Textarea(attrs={'rows': 4}),
    #        'notes': forms.Textarea(attrs={'rows': 4}),
    #    }

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
   comment=forms.CharField(max_length=100,required=False)
   files = MultiFileField()
   
