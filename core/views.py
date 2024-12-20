from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import BranchForm
from .models import Branch
from django.shortcuts import get_object_or_404
def home(request):
    return render(request, "index.html")

def login_view(request):
   form= AuthenticationForm() 
   if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(request, username=username, password=password)
       
       if user is not None:
           login(request, user)
           return redirect('home')  # Redirect to home page after login
       else:
           messages.error(request, 'Invalid username or password')
   return render(request, 'auth/login.html',{'form':form})

@login_required
def logout_view(request):

    
    logout(request)
    return redirect('/')

@login_required
def branch (request):
    
    if request.user.is_superuser:
        form = BranchForm()
        data = Branch.objects.all().order_by('-id')
        if request.method == 'POST' :
            form = BranchForm(request.POST or None)
                   
            if form.is_valid():
                
                form.save()
                
                form = BranchForm()
               
                
                return render(request,'addbranch.html',{'form': form,'data':data,})
              
        return render(request,'addbranch.html',{'form': form,'data':data,})
    else :
        return render(request,'404.html')

@login_required
def branch_update(request, id):
    if request.user.is_superuser:
        branchm= get_object_or_404(Branch, id=id)
        form = BranchForm(request.POST or None, instance=branchm)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Location Updated')
            return redirect('branchs')
        return render(request, 'addbranch.html', {'form':form,'editing':True})
    else :
        return render(request,'404.html')
