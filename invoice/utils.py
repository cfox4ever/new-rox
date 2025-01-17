from django.utils.dateparse import parse_date
from decimal import Decimal
from datetime import date ,datetime
def DateStripper(d):
    d = datetime.strptime(d,"%Y-%m-%d").date()
    return d 
def apply_filters(request, queryset):
    if request.GET.get("branch"):
        queryset = queryset.filter(
            branch=request.GET.get("branch")
        )
    if request.GET.get("vendor"):
        queryset = queryset.filter(vendor=request.GET.get("vendor"))
    if request.GET.get("invoice_number"):
        queryset = queryset.filter(
            invoice_number__icontains=request.GET.get("invoice_number"))
    if request.GET.get("requisition_number"):
        queryset = queryset.filter(
            requisition_number__icontains=request.GET.get("requisition_number")
        )
        
    if request.GET.get("po_number"):
        queryset = queryset.filter(
            po_number__icontains=request.GET.get("po_number")
        )
    if request.GET.get("invoice_date_from"):
        queryset = queryset.filter(
            invoice_date__gt=DateStripper(request.GET.get("invoice_date_from"))
        )
    if request.GET.get("invoice_date_to"):
        queryset = queryset.filter(
            invoice_date__lt=DateStripper(request.GET.get("invoice_date_to"))
        )
    if request.GET.get("req_date_from"):
        queryset = queryset.filter(
            invoice_date__gt=DateStripper(request.GET.get("req_date_from"))
        )
    if request.GET.get("req_date_to"):
        queryset = queryset.filter(
            invoice_date__lt=DateStripper(request.GET.get("req_date_to"))
        )
    if request.GET.get("po_date_from"):
        queryset = queryset.filter(
            invoice_date__gt=DateStripper(request.GET.get("po_date_from"))
        )
    if request.GET.get("po_date_to"):
        queryset = queryset.filter(
            invoice_date__lt=DateStripper(request.GET.get("po_date_to"))
        )
    if request.GET.get("received_date_from"):
        queryset = queryset.filter(
            invoice_date__gt=DateStripper(request.GET.get("received_date_from"))
        )
    if request.GET.get("received_date_to"):
        queryset = queryset.filter(
            invoice_date__lt=DateStripper(request.GET.get("received_date_to"))
        )
    if request.GET.get("ap_date_from"):
        queryset = queryset.filter(
            invoice_date__gt=DateStripper(request.GET.get("ap_date_from"))
        )
    if request.GET.get("ap_date_to"):
        queryset = queryset.filter(
            invoice_date__lt=DateStripper(request.GET.get("ap_date_to"))
        )
    if request.GET.get("vendor_date_from"):
        queryset = queryset.filter(
            invoice_date__gt=DateStripper(request.GET.get("vendor_date_from"))
        )
    if request.GET.get("vendor_date_to"):
        queryset = queryset.filter(
            invoice_date__lt=DateStripper(request.GET.get("vendor_date_to"))
        )
    if request.GET.get("total_form"):
        queryset = queryset.filter(
            total__gt=Decimal(request.GET.get("total_form"))
        )
    if request.GET.get("total_to"):
        queryset = queryset.filter(
            total__lt=Decimal(request.GET.get("total_to"))
        )
    if request.GET.get("grand_total_from"):
        queryset = queryset.filter(
            total__gt=Decimal(request.GET.get("grand_total_from"))
        )
    if request.GET.get("grand_total_to"):
        queryset = queryset.filter(
            total__lt=Decimal(request.GET.get("grand_total_to"))
        )
    
   
        
    if request.GET.get("status"):
        queryset = queryset.filter(
            status=request.GET.get("status")
        )
    if request.GET.get("notes"):
        queryset = queryset.filter(
            notes__icontains=request.GET.get("notes")
        )
    if request.GET.get("follow_up"):
        user = request.user
        print("USER",user)
        queryset = queryset.filter(
           favorited_by =user
        )
    # if request.GET is empty return queryset exclude ststus contains Completed 
    
    return queryset 