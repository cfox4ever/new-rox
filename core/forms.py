from django import forms 
from .models import Branch 
from .setups import STATES,status

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('name', 'phone', 'address_1', 'address_2',
                  'city', 'state', 'zip_code', 'status')

        widgets = {

            'name': forms.TextInput(attrs={'placeholder': 'Branch Name', 'required': True, 'class': "form-control"}),
            'phone': forms.TextInput(attrs={'placeholder': 'Branch main Phone Number', 'required': True, 'class': "form-control"}),
            'address_1': forms.TextInput(attrs={'placeholder': 'Address', 'required': True, 'class': "form-control"}),
            'address_2': forms.TextInput(attrs={'placeholder': 'Address', 'class': "form-control"}),

            'city': forms.TextInput(attrs={'placeholder': 'City', 'required': True, 'class': "form-control"}),
            'state': forms.Select(attrs={'placeholder': 'State', 'required': True, 'class': "form-control"},choices=STATES),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code', 'required': True, 'class': "form-control"}),

            'status': forms.Select(attrs={'placeholder': 'Status', 'required': True, 'class': "select"},choices=status),



        }
    def clean_name(self):
        
        name = self.cleaned_data.get("name")
        if "@" in name :
            
            raise ValidationError( 'Branch Name Invalid.')

        return name 

    # def clean_phone(self):
    #     phone = self.cleaned_data.get("phone")
    #     if len(phone) != 10 or "+" in phone or type(phone) != str :
    #         raise ValidationError ('Please enter a Valid Phone Number ')
    #     return phone