from django.urls import path
from .views import home,login_view,logout_view,branch,branch_update
urlpatterns = [
   path('', home, name='home'),
   path('login/', login_view, name='login'),
   path('logout/',logout_view,name='logout'),
   path('branchs/',branch,name='branchs'),
   path('branch/<int:id>', branch_update ,name='branchupdate'),
   
]