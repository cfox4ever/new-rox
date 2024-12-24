from django.shortcuts import render,redirect, get_object_or_404
from .models import Invoice
from .forms import InvoiceForm
from django.utils.timezone import now 
from django.views.decorators.http import require_http_methods

def invoice_list(request):
   form = InvoiceForm()
   data = Invoice.objects.all()
   if request.method == 'POST':
      form = InvoiceForm(request.POST)
      if form.is_valid:
         form.save()
   return render(request, 'invoice_list.html', {'data': data,'form':form})
def invoice_detail(request, pk):
   invoice = get_object_or_404(Invoice, pk=pk)
   return render(request, 'invoice_detail.html', {'invoice': invoice})

def recieve_now(request,pk):
   
   invoice=get_object_or_404(Invoice,id=pk)
   invoice.received_date = now()
   invoice.save()
  
   return redirect('invoice_list')

def sent_to_ap_date(request,pk):
   invoice=get_object_or_404(Invoice,id=pk)
   invoice.sent_to_ap_date = now()
   invoice.save()
   
   return redirect('invoice_list')

