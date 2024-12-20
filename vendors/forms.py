from django import forms
from .models import Vendor,File
from django.forms.widgets import ClearableFileInput

class VendorForm(forms.ModelForm):
   
   class Meta:
       model = Vendor
       fields = ['branch','name', 'phone', 'email', 'services', 'notes','status']
    #    widgets = {
    #        'services': forms.Textarea(attrs={'rows': 4}),
    #        'notes': forms.Textarea(attrs={'rows': 4}),
    #    }
class FileUploadForm(forms.ModelForm):
   class Meta:
       model = File
       fields = ['file']
class MultiFileInput(ClearableFileInput):
   allow_multiple_selected = True  # Enable multiple file selection
class MultiFileUploadForm(forms.Form):
   files = forms.FileField(
       widget=MultiFileInput(attrs={'multiple': True}),
       label="Upload Files"
   )
