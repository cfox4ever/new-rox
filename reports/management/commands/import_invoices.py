import csv
import json
import os
import urllib.parse
from decimal import Decimal
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware, timezone
from vendors.models import Vendor
from core.models import Branch
from invoice.models import Invoice
from .nuvolo import records
def get_status(status):
   if status == "Quote":
       return 'quote'
   elif status == "No Enty":
       return 'pending'
   elif status == "PO":
       return 'po'
   elif status == "Received":
       return 'received'
   elif status == "Requisition":
       return 'requisition'
   elif status == "Sent To AP":
       return 'sent_to_ap'
   elif status == "Canceled":
       return 'cancelled'
   elif status == "Rejected":
       return 'rejected'
   else:
       return 'unknown'  # Fallback for missing or invalid status
def get_vendor(vendor_name):
   try:
       vendor = Vendor.objects.get(name=vendor_name)
       return vendor
   except Vendor.DoesNotExist:
       print(f"Vendor not found: {vendor_name}")
       return None
def get_total(total):
   if total is not None:
       total = total.replace("$", '')
       t = total.strip()
       if t:
           return Decimal(t)
   return Decimal('0.00')
def format_date(date_string):
   if not date_string or date_string.strip() == '':
       return None  # Return None for empty or invalid dates
   try:
       parsed_date = datetime.strptime(date_string, "%m/%d/%Y")
       aware_date = make_aware(parsed_date, timezone.utc)
       return aware_date
   except ValueError as e:
       raise ValueError(f"Invalid date format for '{date_string}'. Expected MM/DD/YYYY. Error: {e}")

def find_record(data, key,value):
   for record in data["records"]:
    #    print("RECORD",record)
       if record["number"] == value:
           return record
   return None
    # Example usage
    # target_number = "FPO0083549"
    # found_record = find_record_by_number(data["records"], target_number)
    # if found_record:
    # print("Record found:", found_record)
    # else:
    # print("Record not found.")

import re

def get_url( requisition_number, params=None):
   base_url = "https://phsi.service-now.com/now/nav/ui/classic/params/target/x_nuvo_eam_facilities_purchase_order.do"
   current_dir = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(current_dir, 'nuvolo.json') 
  
   with open(file_path, mode='r') as f:
        data = json.load(f)
        key = 'number'
        value = requisition_number
        record = find_record(data, key, value)
        if record:
            print("Record found:", record)
        else:
            print("Record not found.")
   sys_id = record.get("sys_id", "")
   u_hospital = record.get("u_hospital", "")
   number = record.get("number", "")
   url = (
       f"{base_url}?sys_id={sys_id}"
       f"&sysparm_view=AssetUser"
       f"&sysparm_record_target=x_nuvo_eam_facilities_purchase_order"
       f"&sysparm_record_row=1"
       f"&sysparm_record_rows=1"
       f"&sysparm_record_list=u_hospital={u_hospital}^numberSTARTSWITH{number}^ORDERBYDESCsys_created_on"
   )
   return url





class Command(BaseCommand):
   ur = get_url("FPO0083549") 
   print(ur)
   help = "Import invoices from a CSV file"
   def handle(self, *args, **kwargs):
       current_dir = os.path.dirname(os.path.abspath(__file__))
       file_path = os.path.join(current_dir, 'invoices.csv')
       try:
           with open(file_path, mode='r', encoding='windows-1252') as file:
               reader = csv.DictReader(file)
               for row in reader:
                   vendor_name = row['vendor']
                   vendor = get_vendor(vendor_name)
                   if not vendor:
                       continue
                   requisition_date = self.parse_date(row.get('requisition_date'))
                   po_date = self.parse_date(row.get('po_date'))
                   invoice_date = self.parse_date(row.get('invoice_date'))
                   received_date = self.parse_date(row.get('received_date'))
                   sent_to_ap_date = self.parse_date(row.get('sent_to_ap_date'))
                   total = self.parse_decimal(row.get('total2'))
                   shipping = self.parse_decimal(row.get('shipping'))
                   tax = self.parse_decimal(row.get('tax'))
                #    Invoice.objects.create(
                #        branch=Branch.objects.get(id=1),  # Update this if branch is required
                #        vendor=vendor,
                #        invoice_number=row.get('invoice_number'),
                #        quote_number=row.get('quote_number'),
                #        total=total,
                #        shipping=shipping,
                #        tax=tax,
                #        requisition_number=row.get('requisition_number'),
                #        requisition_date=requisition_date,
                #        po_number=row.get('po_number'),
                #        po_date=po_date,
                #        invoice_date=invoice_date,
                #        received_date=received_date,
                #        sent_to_ap_date=sent_to_ap_date,
                #        notes=row.get('notes'),
                #        status=get_status(row.get('status')),
                #        url=get_url(row.get('requisition_number'))
                #    )
                   self.stdout.write(f"Invoice {row.get('invoice_number')} imported successfully!")
       except Exception as e:
           self.stderr.write(f"Error: {e}")
   def parse_date(self, date_str):
       if date_str:
           try:
               naive_date = datetime.strptime(date_str.strip(), '%m/%d/%Y')
               return make_aware(naive_date)
           except ValueError:
               self.stderr.write(f"Invalid date format: {date_str}")
       return None
   def parse_decimal(self, value):
       if value:
           try:
               return Decimal(value.replace("$", "").replace(",", "").strip())
           except ValueError:
               self.stderr.write(f"Invalid decimal value: {value}")
       return None