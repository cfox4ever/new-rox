from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Invoice,
    QuoteFile,
    InvoiceFile,
    RequisitionFile,
    ReceivedFile,
    POFile,
    EmailFile,
    Contract,
    ContractFile,
)
from vendors.models import Vendor
from .forms import InvoiceForm, MultiFileUploadForm, ContractForm
from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import apply_filters
from urllib.parse import urlencode
from core.models import Branch
from decimal import Decimal 
#### ARCHIVE Imports ####
from .models import ArchiveFile


from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter

from PyPDF2 import PdfMerger, PdfReader

from docx import Document

from docx2pdf import convert

from PIL import Image

import pandas as pd

import io

import os

from datetime import datetime
from django.utils.dateformat import format as date_format
from django.utils.timezone import localtime

@login_required
def invoice_list(request):
    page = request.GET.get("page", 1)
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():  # Call is_valid() as a method
            contract_number = form.cleaned_data['contract']
            invoice_total = form.cleaned_data['total']
            instance = form.save(commit=False)
            instance.created_by=request.user
            instance.save()
            
            if contract_number :
                # contract = Contract.objects.get(contract_number=contract_number)
                contract = contract_number
                contract.created_by=request.user
                contract.total_invoices_to_date = Decimal(contract.total_invoices_to_date or 0) + Decimal(invoice_total or 0)
                contract.save() 
            
            
    else:
        form = InvoiceForm()

    data = Invoice.objects.all()
    vendors = Vendor.objects.all()
    branches = Branch.objects.all()
    paginator = Paginator(data, 15)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    def get_page_url(page_number):
        params = request.GET.copy()
        params["page"] = page_number
        return "?" + urlencode(params)

    if request.htmx:
        data = Invoice.objects.all()
        data = apply_filters(request, data)

        context = {"data": data}
        return render(request, "partials/table.html", context)

    context = {"data": data, "form": form, "vendors": vendors, "branches": branches}
    return render(request, "invoice_list.html", context)


@login_required
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    old_invoice_total = invoice.total
    vendors = Vendor.objects.all()
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            new_invoice_total = form.cleaned_data['total'] or 0 
            contract_number= form.cleaned_data['contract'] or None 
            form.save()
            if contract_number :
                # contract = Contract.objects.get(contract_number=contract_number)
                contract = contract_number
                contract.total_invoices_to_date = Decimal(contract.total_invoices_to_date) - Decimal(old_invoice_total) +  Decimal(new_invoice_total)
                contract.save()
            return redirect("invoice_list")
    else:
        form = InvoiceForm(instance=invoice)
    editing = True
    return render(
        request,
        "invoice_edit.html",
        {"form": form, "vendors": vendors, "editing": editing},
    )


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, "invoice_detail.html", {"invoice": invoice})


@login_required
def recieve_now(request, pk):

    invoice = get_object_or_404(Invoice, id=pk)
    invoice.received_date = now()
    invoice.save()

    return redirect("invoice_list")


@login_required
def sent_to_ap_date(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice.sent_to_ap_date = now()
    invoice.save()

    return redirect("invoice_list")


################ QUOTE FILES ##########################


@login_required
def add_quote(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
   
    files = QuoteFile.objects.filter(invoice=invoice)
    if request.method == "POST":
        form = MultiFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist("files")
            for uploaded_file in uploaded_files:
                QuoteFile.objects.create(
                    invoice=invoice, file=uploaded_file, created_by=request.user
                )
            return redirect("add_quote", pk=invoice.id)
    else:
        form = MultiFileUploadForm()
    return render(
        request,
        "quote_files.html",
        {"invoice": invoice, "files": files, "form": form, "file_type": "Quote"},
    )


@login_required
def delete_quote_file(request, pk):
    file = get_object_or_404(QuoteFile, id=pk)
    invoice_id = file.invoice.id
    file.delete()
    return redirect("add_quote", pk=invoice_id)


############## INVOICE FILES ################################


@login_required
def add_invoice(request, pk):
   
    invoice = get_object_or_404(Invoice, id=pk)
    files = InvoiceFile.objects.filter(invoice=invoice)
    
    if request.method == "POST":
        form = MultiFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist("files")
            for uploaded_file in uploaded_files:
                InvoiceFile.objects.create(
                    invoice=invoice, file=uploaded_file, created_by=request.user
                )
            return redirect("add_invoice", pk=invoice.id)
    else:
        form = MultiFileUploadForm()
    return render(
        request,
        "quote_files.html",
        {"invoice": invoice, "files": files, "form": form, "file_type": "Invoice"},
    )


@login_required
def delete_invoice_file(request, pk):
    file = get_object_or_404(InvoiceFile, id=pk)
    invoice_id = file.invoice.id
    file.delete()
    return redirect("add_invoice", pk=invoice_id)


################## REQ FILES ###############


@login_required
def add_req(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    files = RequisitionFile.objects.filter(invoice=invoice)
    if request.method == "POST":
        form = MultiFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist("files")
            for uploaded_file in uploaded_files:
                RequisitionFile.objects.create(
                    invoice=invoice, file=uploaded_file, created_by=request.user
                )
            return redirect("add_req", pk=invoice.id)
    else:
        form = MultiFileUploadForm()
    return render(
        request,
        "quote_files.html",
        {"invoice": invoice, "files": files, "form": form, "file_type": "Requestion"},
    )


@login_required
def delete_req_file(request, pk):
    file = get_object_or_404(RequisitionFile, id=pk)
    invoice_id = file.invoice.id
    file.delete()
    return redirect("add_req", pk=invoice_id)


################# PO FILES ############


@login_required
def add_po(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    files = POFile.objects.filter(invoice=invoice)
    if request.method == "POST":
        form = MultiFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist("files")
            for uploaded_file in uploaded_files:
                POFile.objects.create(
                    invoice=invoice, file=uploaded_file, created_by=request.user
                )
            return redirect("add_po", pk=invoice.id)
    else:
        form = MultiFileUploadForm()
    return render(
        request,
        "quote_files.html",
        {"invoice": invoice, "files": files, "form": form, "file_type": "PO"},
    )


@login_required
def delete_po_file(request, pk):
    file = get_object_or_404(POFile, id=pk)
    invoice_id = file.invoice.id
    file.delete()
    return redirect("add_po", pk=invoice_id)


################# RECIVED FILES ############


@login_required
def add_recieve(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    files = ReceivedFile.objects.filter(invoice=invoice)
    if request.method == "POST":
        form = MultiFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist("files")
            for uploaded_file in uploaded_files:
                ReceivedFile.objects.create(
                    invoice=invoice, file=uploaded_file, created_by=request.user
                )
            return redirect("add_recieve", pk=invoice.id)
    else:
        form = MultiFileUploadForm()
    return render(
        request,
        "quote_files.html",
        {"invoice": invoice, "files": files, "form": form, "file_type": "Received"},
    )


@login_required
def delete_recieve_file(request, pk):
    file = get_object_or_404(ReceivedFile, id=pk)
    invoice_id = file.invoice.id
    file.delete()
    return redirect("add_recieve", pk=invoice_id)


################# EMAIL FILES ############


@login_required
def add_email(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    files = EmailFile.objects.filter(invoice=invoice)
    if request.method == "POST":
        form = MultiFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist("files")
            for uploaded_file in uploaded_files:
                EmailFile.objects.create(
                    invoice=invoice, file=uploaded_file, created_by=request.user
                )
            return redirect("add_email", pk=invoice.id)
    else:
        form = MultiFileUploadForm()
    return render(
        request,
        "quote_files.html",
        {"invoice": invoice, "files": files, "form": form, "file_type": "EMAIL"},
    )


@login_required
def delete_email_file(request, pk):
    file = get_object_or_404(EmailFile, id=pk)
    invoice_id = file.invoice.id
    file.delete()
    return redirect("add_email", pk=invoice_id)


################# ARCHIVE FILES ############


@login_required
def create_archive_for_invoice(request, invoice_id):
    """
    Create an archive containing all files related to an invoice.
    """
    # Fetch the invoice object
    invoice = get_object_or_404(Invoice, id=invoice_id)
    # Temporary directory for processing
    temp_dir = f"temp_archive_{invoice_id}"
    os.makedirs(temp_dir, exist_ok=True)
    try:
        # Create a summary PDF
        summary_path = os.path.join(temp_dir, "summary.pdf")
        create_summary_pdf(invoice, summary_path)
        # Initialize a list of PDFs
        pdf_files = [summary_path]
        # Define file groups
        file_groups = [
            ("Quote", invoice.quote_files.all()),
            ("Invoice", invoice.invoice_files.all()),
            ("Requisition", invoice.requisition_files.all()),
            ("PO", invoice.po_files.all()),
            ("Received", invoice.received_files.all()),
        ]
        # Process each group
        for prefix, files in file_groups:
            for idx, file_obj in enumerate(files):
                if not file_obj.file:
                    continue
                file_path = file_obj.file.path
                output_pdf = os.path.join(temp_dir, f"{prefix}_{idx}.pdf")
                # Handle different file types
                if file_path.lower().endswith(".pdf"):
                    pdf_files.append(file_path)
                elif file_path.lower().endswith((".doc", ".docx")):
                    convert_word_to_pdf(file_path, output_pdf)
                    pdf_files.append(output_pdf)
                elif file_path.lower().endswith((".xls", ".xlsx")):
                    convert_excel_to_pdf(file_path, output_pdf)
                    pdf_files.append(output_pdf)
                elif file_path.lower().endswith((".jpg", ".jpeg", ".png")):
                    convert_image_to_pdf(file_path, output_pdf)
                    pdf_files.append(output_pdf)
        # Merge all PDFs
        output_path = os.path.join(temp_dir, f"archive_{invoice_id}.pdf")
        merge_pdfs(pdf_files, output_path)
        # Save to ArchiveFile model
        archive_file = ArchiveFile.objects.create(
            invoice=invoice, number=invoice.invoice_number, created_by=request.user
        )
        with open(output_path, "rb") as f:
            archive_file.file.save(f"archive_{invoice_id}.pdf", io.BytesIO(f.read()))
        return redirect("invoice_list")
    finally:
        # Clean up temporary files
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)


def create_summary_pdf(invoice, output_path):
    """Creates a PDF summary of the invoice details"""

    c = canvas.Canvas(output_path, pagesize=letter)

    y = 750  # Starting y position

    # Add header

    c.setFont("Helvetica-Bold", 16)

    c.drawString(50, y, f"Invoice Summary - {invoice.vendor.name}")

    y -= 30

    # Add invoice details

    details = [
        ("Invoice Number:", invoice.invoice_number),
        ("PO Number:", invoice.po_number),
        ("Requisition Number:", invoice.requisition_number),
        ("Grand Total:", f"${invoice.grand_total:,.2f}"),
        ("Requisition Date:", format_date(invoice.requisition_date)),
        ("PO Date:", format_date(invoice.po_date)),
        ("Received Date:", format_date(invoice.received_date)),
        ("Sent to AP Date:", format_date(invoice.sent_to_ap_date)),
        ("Sent to Vendor Date:", format_date(invoice.send_to_vendor_date)),
    ]

    c.setFont("Helvetica", 12)

    for label, value in details:

        c.drawString(50, y, f"{label} {value or 'N/A'}")

        y -= 20

    c.save()


def convert_word_to_pdf(input_path, output_path):
    """Converts Word documents to PDF"""

    convert(input_path, output_path)


def convert_excel_to_pdf(input_path, output_path):
    """Converts Excel files to PDF."""
    # Choose the appropriate engine
    if input_path.endswith(".xls"):
        engine = "xlrd"
    else:  # For .xlsx
        engine = "openpyxl"
    # Read the Excel file
    try:
        df = pd.read_excel(input_path, engine=engine)
    except ImportError as e:
        raise ImportError(f"Error reading Excel file: {e}")
    # Convert DataFrame to HTML
    html = df.to_html()
    # Convert HTML to PDF using reportlab
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica", 10)
    # Render the HTML table on the PDF
    y = 750
    for line in html.split("\n"):
        if y < 50:  # Start a new page if near the bottom
            c.showPage()
            y = 750
        c.drawString(50, y, line.strip())
        y -= 12
    c.save()


def convert_image_to_pdf(input_path, output_path):
    """Converts images to PDF"""

    image = Image.open(input_path)

    if image.mode == "RGBA":

        image = image.convert("RGB")

    image.save(output_path, "PDF")


def merge_pdfs(input_paths, output_path):
    """Merges multiple PDFs into a single file"""

    merger = PdfMerger()

    for path in input_paths:

        if os.path.exists(path):

            try:

                merger.append(PdfReader(open(path, "rb")))

            except Exception as e:

                print(f"Error merging PDF {path}: {str(e)}")

    merger.write(output_path)

    merger.close()


def format_date(date):
    """Formats datetime object to string"""

    return date.strftime("%Y-%m-%d") if date else "N/A"


@login_required
def toggle_favorite(request, invoice_id):
    if request.method == "POST":
        invoice = get_object_or_404(
            Invoice.objects.prefetch_related("favorited_by"), id=invoice_id
        )
        # Check if user has already favorited
        if invoice.favorited_by.filter(id=request.user.id).exists():
            invoice.favorited_by.remove(request.user)
        else:
            invoice.favorited_by.add(request.user)
        return redirect("invoice_list")
    return redirect("invoice_list")


@login_required
def send_to_vendor(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice.send_to_vendor_date = now()
    invoice.send_to_vendor = False
    invoice.save()

    return redirect("invoice_list")


############ CONTRACT ##########
@login_required
def contract_list(request):
    page = request.GET.get("page", 1)
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():  # Call is_valid() as a method
            form.save()
    else:
        form = ContractForm()

    data = Contract.objects.all()
    vendors = Vendor.objects.all()
    branches = Branch.objects.all()
    paginator = Paginator(data, 15)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    def get_page_url(page_number):
        params = request.GET.copy()
        params["page"] = page_number
        return "?" + urlencode(params)

    if request.htmx:
        data = Contract.objects.all()
        data = apply_filters(request, data)

        context = {"data": data}
        return render(request, "partials/contract_table.html", context)

    context = {"data": data, "form": form, "vendors": vendors, "branches": branches}
    return render(request, "contract_list.html", context)


@login_required
def contract_toggle_favorite(request, contract_id):
    if request.method == "POST":
        contract = get_object_or_404(
            Contract.objects.prefetch_related("favorited_by"), id=contract_id
        )
        # Check if user has already favorited
        if contract.favorited_by.filter(id=request.user.id).exists():
            contract.favorited_by.remove(request.user)
        else:
            contract.favorited_by.add(request.user)
        return redirect("contract_list")
    return redirect("contract_list")


@login_required
def send_contract_to_vendor(request, pk):
    contract = get_object_or_404(Contract, id=pk)
    contract.send_to_vendor_date = now()
    contract.send_to_vendor = False
    contract.save()

    return redirect("contract_list")


@login_required
def edit_contract(request, pk):
    contract = get_object_or_404(Contract, id=pk)
    vendors = Vendor.objects.all()
    if request.method == "POST":
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()
            return redirect("contract_list")
    else:
        form = ContractForm(instance=contract)
    editing = True
    return render(
        request,
        "contract_edit.html",
        {"form": form, "vendors": vendors, "editing": editing},
    )


################# CONTRACT FILES ############


@login_required
def add_contract(request, pk):
    contract = get_object_or_404(Contract, id=pk)
    files = ContractFile.objects.filter(contract=contract)
    if request.method == "POST":
        form = MultiFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist("files")
            for uploaded_file in uploaded_files:
                ContractFile.objects.create(
                    contract=contract, file=uploaded_file, created_by=request.user
                )
            return redirect("add_contract", pk=contract.id)
    else:
        form = MultiFileUploadForm()
    return render(
        request,
        "quote_files.html",
        {"contract": contract, "files": files, "form": form, "file_type": "CONTRACT"},
    )


@login_required
def delete_contract_file(request, pk):
    file = get_object_or_404(ContractFile, id=pk)

    contract_id = file.contract.id
    file.delete()

    return redirect("add_contract", pk=contract_id)


#### INVOICE FORM HTMX ####


@login_required
def create_invoice_form(request):
    invoice_type = request.POST.get("invoice_type")
    if invoice_type == "invoice":
        form = InvoiceForm()
        vs = Vendor.objects.all()
    if invoice_type == "contract":
        return HttpResponse("")
    return render(request, "partials/invoice_form.html", {"form": form, "vs": vs})


@login_required
def vendor_contracts(request):
    vendor_id = request.POST.get("vendor")
    vendor = get_object_or_404(Vendor, id=vendor_id)
    contracts = Contract.objects.filter(vendor=vendor)
    print(contracts)
    if len(contracts) == 0:
        return HttpResponse("No contracts found for this vendor")
    return render(
        request,
        "partials/vendor_contracts.html",
        {
            "contracts": contracts,
        },
    )


@login_required
def invoice_for_contract(request):
    contract_id = request.POST.get("contract")
    contract = get_object_or_404(Contract, id=contract_id)
    similar_between_inv_contract = {
        "branch": contract.branch,
        "vendor": contract.vendor,
        "po_number": contract.po_number,
        "requisition_number": contract.requisition_number,
        "quote_number": contract.quote_number,
        "requisition_date": contract.requisition_date,
        "po_date": contract.po_date,
        "send_to_vendor_date": contract.send_to_vendor_date,
        "url": contract.url,
        "status": "contract_invoice",
        "contract":contract,
    }
    form = InvoiceForm(initial=similar_between_inv_contract)
    return render(
        request,
        "partials/invoice_form.html",
        {
            "form": form,
        },
    )




def format_date_if_needed(value):
   """
   Helper function to format date-like strings into human-readable format.
   """
   from dateutil.parser import parse
   from datetime import datetime
   if isinstance(value, (datetime,)):
# If already a datetime, format it directly
       return date_format(localtime(value), "l, F j, Y h:i A")
   try:
# Attempt to parse the value as a date
       parsed_date = parse(value)
       return parsed_date.strftime("%A, %B %d, %Y %I:%M %p")
   except (ValueError, TypeError):
# Return the value as-is if it's not a date
       return value


@login_required
def invoice_history(request, pk):
   invoice = get_object_or_404(Invoice, id=pk)
   history = invoice.history.all()
   parsed_logs = []
   for i in range(1, len(history)):
       new_record = history[i]
       old_record = history[i - 1]
       delta = new_record.diff_against(old_record)
       for change in delta.changes:
# Format the date fields if applicable
           old_value = format_date_if_needed(change.old)
           new_value = format_date_if_needed(change.new)
           changed_at = localtime(new_record.history_date)
           changed_at_formatted = date_format(changed_at, "l, F j, Y h:i A")
           parsed_logs.append({
               "field": change.field,
               "changed_from": old_value,
               "changed_to": new_value,
               "by": new_record.history_user,
               "date": changed_at_formatted,
           })
   return render(request, "invoice_history.html", {"h": parsed_logs})