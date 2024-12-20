from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Vendor,File
from .forms import VendorForm,MultiFileUploadForm
from django.shortcuts import render,redirect,get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required


@login_required
def vendor_create(request):
    form = VendorForm()
    data = Vendor.objects.all()
    
    context= {'form':form,'data':data} 
    if request.method == 'POST' :
            form = VendorForm(request.POST,request.FILES or None)
            files = request.FILES.getlist('file')       
            if form.is_valid():
                try:
                    with transaction.atomic():  # Ensure atomic transaction
                        # Save Vendor instance
                        vendor = form.save(commit=False)
                        vendor.save()
                        # Save uploaded files associated with the Vendor
                        for f in files:
                            File.objects.create(vendor=vendor, file=f)
                except Exception as e:
                    print(e)
                form = VendorForm()
               
                
                return render (request,'add_vendor.html',context)
              
    return render(request,'add_vendor.html',context)



             
def vendor_edit(request,pk):
    vendor = Vendor.objects.get(id=pk)
    form = VendorForm(instance=vendor)
    
    context= {'form':form} 
    if request.method == 'POST' :
            form = VendorForm(request.POST,request.FILES,instance=vendor or None)
            files = request.FILES.getlist('file')       
            if form.is_valid():
                try:
                    with transaction.atomic():  # Ensure atomic transaction
                        # Save Vendor instance
                        vendor = form.save(commit=False)
                        vendor.save()
                        # Save uploaded files associated with the Vendor
                        for f in files:
                            File.objects.create(vendor=vendor, file=f)
                except Exception as e:
                    print(e)
                form = VendorForm()
            
                
                return redirect('vendors')
            
    return render(request,'add_vendor.html',context)

   



def vendor_files(request, vendor_id):
   vendor = get_object_or_404(Vendor, id=vendor_id)
   files = vendor.vendor_files.all()  # Assuming related_name="vendor_files"
   if request.method == 'POST':
       form = MultiFileUploadForm(request.POST, request.FILES)
       if form.is_valid():
           uploaded_files = request.FILES.getlist('files')
           for uploaded_file in uploaded_files:
               File.objects.create(vendor=vendor, file=uploaded_file)
           return redirect('vendor_files', vendor_id=vendor.id)
   else:
       form = MultiFileUploadForm()
   return render(request, 'vendor_files.html', {'vendor': vendor, 'files': files, 'form': form})

def delete_file(request, file_id):
   file = get_object_or_404(File, id=file_id)
   vendor_id = file.vendor.id
   file.delete()
   return redirect('vendor_files', vendor_id=vendor_id)