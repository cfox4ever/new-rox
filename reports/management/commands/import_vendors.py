import csv
import os
from django.core.management.base import BaseCommand

from vendors.models import Vendor 
from core.models import Branch 
from django.contrib.auth.models import User
class Command(BaseCommand):
   help = "Import vendors from a CSV file"
   def handle(self, *args, **kwargs):
       file_name = "vendors.csv"
       file_path = os.path.join(os.path.dirname(__file__), file_name)
       try:
            # for i in range(5,200):
            #     if Vendor.objects.filter(id=i).exists():
            #         Vendor.objects.get(id=i).delete()


           with open(file_path, newline='', encoding='utf-8-sig') as csvfile:  # Use 'utf-8-sig' to handle BOM
               reader = csv.DictReader(csvfile)
               # Debug: Print the headers
               self.stdout.write(f"CSV Headers: {reader.fieldnames}")
               branch= Branch.objects.get(id=1)
               user = User.objects.get(id=1)
               for row in reader:
                   # Debug: Print each row
                   self.stdout.write(f"Row: {row}")
                   name = row.get('name', '').strip()
                   phone = row.get('phone', '').strip()
                   email = row.get('email', '').strip()
                   service = row.get('service', '').strip()
                   contact = row.get('contact', '').strip()
                   if not name:  # Skip rows without a name
                       self.stdout.write(self.style.WARNING(f"Skipping row due to missing 'name': {row}"))
                       continue
                   Vendor.objects.create(
                       branch=branch,
                       created_by=user,
                       status="active",                      
                       name=name,
                       phone=phone,
                       email=email if email != 'None' else '',
                       services=service,
                       notes=contact if contact != 'None' else '',
                   )
                   self.stdout.write(self.style.SUCCESS(f"Imported vendor: {name}"))
    # except FileNotFoundError:
    #        self.stdout.write(self.style.ERROR(f"File {file_name} does not exist in the current folder."))
       except Exception as e:
           self.stdout.write(self.style.ERROR(f"Error importing vendors: {e}"))