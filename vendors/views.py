from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Vendor,File
from .forms import VendorForm,MultiFileUploadForm
from django.shortcuts import render,redirect,get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from core.models import Branch
from django.db.models import Q

STATUS_CHOICES = ['Pending','On Hold','Active','In-Active']
@login_required
def vendor_create(request):
    form = VendorForm()
    data = Vendor.objects.all()
    user = request.user
    branches = Branch.objects.all()
    status_choices = STATUS_CHOICES

    branch = request.GET.get('branch')
    name = request.GET.get('name')
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    services = request.GET.get('services')
    notes = request.GET.get('notes')
    status = request.GET.get('status')
    if request.method == 'GET':

        if branch:
           data= data.filter(branch__id=branch)
        if name :
            
           data= data.filter(name__icontains=name)
        if phone :
            data.filter(phone__icontains=phone)
        if email :
            data=data.filter(email__icontains=email)
        if services :
           data= data.filter(services__icontains=services)
        if notes :
           data= data.filter(notes__icontains=notes)
        if status :
           data= data.filter(status__icontains=status)

    
    context= {'form':form,'data':data,'branches':branches,
    'status_choices':status_choices} 
    if request.method == 'POST' :
            form = VendorForm(request.POST,request.FILES or None)
            uploaded_files = request.FILES.getlist('file')       
            if form.is_valid():
                try:
                    with transaction.atomic():  # Ensure atomic transaction
                        # Save Vendor instance
                        vendor = form.save(commit=False)
                        vendor.created_by = user
                        vendor.save()
                        vendor_name = vendor.name.replace(" ", "_").upper()
                        last_file = File.objects.filter(vendor=vendor).last()

                        if last_file :
                            x = last_file.id
                        else :
                            x = 0
                        for uploaded_file in uploaded_files:
                            # rename the file vendor name capital letters + x 
                            original_extension = uploaded_file.name.split('.')[-1]
                            new_filename = f"{vendor_name}_{x+1}.{original_extension}"
                            uploaded_file.name = new_filename
                            File.objects.create(vendor=vendor, file=uploaded_file,created_by=user)
                            x = x +1 
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
   files = File.objects.filter(vendor=vendor)  # Assuming related_name="vendor_files"
   if request.method == 'POST':
       form = MultiFileUploadForm(request.POST, request.FILES)
       if form.is_valid():
           uploaded_files = request.FILES.getlist('files')
           vendor_name = vendor.name.replace(" ", "_").upper()
           last_file = File.objects.filter(vendor=vendor).last()
           comment = form.cleaned_data['comment']
           x = last_file.id
           for uploaded_file in uploaded_files:
               original_extension = uploaded_file.name.split('.')[-1]
               new_filename = f"{vendor_name}_{x+1}.{original_extension}"
               uploaded_file.name = new_filename

               
               File.objects.create(vendor=vendor, file=uploaded_file,comment=comment,created_by=request.user)
               x= x +1
           return redirect('vendor_files', vendor_id=vendor.id)
   else:
       form = MultiFileUploadForm()
   return render(request, 'vendor_files.html', {'vendor': vendor, 'files': files, 'form': form})

def delete_file(request, file_id):
   file = get_object_or_404(File, id=file_id)
   vendor_id = file.vendor.id
   file.delete()
   return redirect('vendor_files', vendor_id=vendor_id)