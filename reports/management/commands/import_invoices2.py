import csv

import json

import os

import logging

from decimal import Decimal

from django.core.management.base import BaseCommand

from django.db import transaction

from django.utils.timezone import make_aware

from datetime import datetime

from vendors.models import Vendor

from invoice.models import Invoice

logger = logging.getLogger(__name__)

def get_status(status):

    status_mapping = {

        "Quote": "quote",

        "No Entry": "pending",

        "PO": "po",

        "Received": "received",

        "Requisition": "requisition",

        "Sent To AP": "sent_to_ap",

        "Canceled": "cancelled",

        "Rejected": "rejected",

    }

    return status_mapping.get(status, "unknown")

def format_date(date_string):

    if not date_string:

        return None

    try:

        parsed_date = datetime.strptime(date_string.strip(), "%m/%d/%Y")

        return make_aware(parsed_date)

    except ValueError:

        logger.warning(f"Invalid date format: {date_string}")

        return None

def parse_decimal(value):

    if value:

        try:

            return Decimal(value.replace("$", "").replace(",", "").strip())

        except (ValueError, AttributeError):

            logger.warning(f"Invalid decimal value: {value}")

    return Decimal("0.00")

def load_json_file(file_path):

    try:

        with open(file_path, "r", encoding="utf-8") as file:

            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError) as e:

        logger.error(f"Error reading JSON file {file_path}: {e}")

        return None

def get_vendor(name):

    return Vendor.objects.get_or_create(name=name)[0]

class Command(BaseCommand):

    help = "Import invoices from a CSV file"

    def handle(self, *args, **kwargs):

        current_dir = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(current_dir, 'invoices.csv')

        json_path = os.path.join(os.path.dirname(__file__), "nuvolo.json")

        json_data = load_json_file(json_path)

        if not json_data:

            self.stderr.write("Failed to load JSON data. Aborting.")

            return

        try:

            with open(file_path, mode='r', encoding='windows-1252') as file:

                reader = csv.DictReader(file)

                with transaction.atomic():

                    for row in reader:

                        self.process_row(row, json_data)

        except Exception as e:

            logger.error(f"Error processing file {file_path}: {e}")

            self.stderr.write(f"Error: {e}")

    def process_row(self, row, json_data):

        try:

            vendor = get_vendor(row["vendor"])

            requisition_date = format_date(row.get("requisition_date"))

            po_date = format_date(row.get("po_date"))

            invoice_date = format_date(row.get("invoice_date"))

            received_date = format_date(row.get("received_date"))

            sent_to_ap_date = format_date(row.get("sent_to_ap_date"))

            total = parse_decimal(row.get("total2"))

            shipping = parse_decimal(row.get("shipping"))

            tax = parse_decimal(row.get("tax"))

            requisition_number = row.get("requisition_number")

            url = self.get_url(requisition_number, json_data)

            Invoice.objects.create(

                vendor=vendor,

                invoice_number=row.get("invoice_number"),

                quote_number=row.get("quote_number"),

                total=total,

                shipping=shipping,

                tax=tax,

                requisition_number=requisition_number,

                requisition_date=requisition_date,

                po_number=row.get("po_number"),

                po_date=po_date,

                invoice_date=invoice_date,

                received_date=received_date,

                sent_to_ap_date=sent_to_ap_date,

                notes=row.get("notes"),

                status=get_status(row.get("status")),

                url=url,

            )

            self.stdout.write(f"Invoice {row.get('invoice_number')} imported successfully!")

        except Exception as e:

            logger.error(f"Error processing row: {row}. Error: {e}")

    def get_url(self, requisition_number, json_data):

        if isinstance(json_data, dict) and "records" in json_data:  # Check if json_data is a dictionary and has "records"

            records = json_data["records"]  # Access the list of records

            if isinstance(records, list):  # Ensure records is a list

                for item in records:

                    if isinstance(item, dict) and item.get("number") == requisition_number:

                        sys_id = item.get("sys_id")

                        if sys_id:

                            return f"https://phsi.service-now.com/now/nav/ui/classic/params/target/x_nuvo_eam_facilities_purchase_order.do%3Fsys_id%3D{sys_id}"

        return None

 