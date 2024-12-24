from django.urls import path
from .views import vendor_create,vendor_edit,delete_file,vendor_files
urlpatterns = [
 
   path('vendors/',vendor_create,name='vendors'),
   path("edit_vendor/<int:pk>", vendor_edit, name="edit_vendor"),
   # path('vendors/<int:vendor_id>/upload/', upload_vendor_files, name='upload_vendor_files'),
   path('vendors/<int:vendor_id>/files/', vendor_files, name='vendor_files'),
   path('files/<int:file_id>/delete/', delete_file, name='delete_file'),
  
   
]