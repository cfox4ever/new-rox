from django.urls import path
from . import views

urlpatterns = [
    path("", views.invoice_list, name="invoice_list"),
    path("<int:pk>/", views.invoice_detail, name="invoice_detail"),
    path("recieve_now/<int:pk>/", views.recieve_now, name="recieve_now"),
    path("sent_to_ap_date/<int:pk>/", views.sent_to_ap_date, name="sent_to_ap_date"),
    path("add_quote/<int:pk>/", views.add_quote, name="add_quote"),
    path(
        "delete_quote_file/<int:pk>/", views.delete_quote_file, name="delete_quote_file"
    ),
    path("add_invoice/<int:pk>/", views.add_invoice, name="add_invoice"),
    path(
        "delete_invoice_file/<int:pk>/",
        views.delete_invoice_file,
        name="delete_invoice_file",
    ),
    path("add_req/<int:pk>/", views.add_req, name="add_req"),
    path("delete_req_file/<int:pk>/", views.delete_req_file, name="delete_req_file"),
    path("add_po/<int:pk>/", views.add_po, name="add_po"),
    path("delete_po_file/<int:pk>/", views.delete_po_file, name="delete_po_file"),
    path("add_recieve/<int:pk>/", views.add_recieve, name="add_recieve"),
    path(
        "delete_recieve_file/<int:pk>/",
        views.delete_recieve_file,
        name="delete_recieve_file",
    ),
    path("add_email/<int:pk>/", views.add_email, name="add_email"),
    path(
        "delete_email_file/<int:pk>/", views.delete_email_file, name="delete_email_file"
    ),
    path("archive/<int:invoice_id>/", views.create_archive_for_invoice, name="archive"),
    path(
        "invoices/<int:invoice_id>/favorite/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    path("send_to_vendor/<int:pk>/", views.send_to_vendor, name="send_to_vendor"),
    path("edit_invoice/<int:pk>/", views.edit_invoice, name="edit_invoice"),
    path("contracts", views.contract_list, name="contract_list"),
    path(
        "contracts/<int:contract_id>/favorite/",
        views.contract_toggle_favorite,
        name="contract_toggle_favorite",
    ),
    path(
        "send_contract_to_vendor/<int:pk>/",
        views.send_contract_to_vendor,
        name="send_contract_to_vendor",
    ),
    path("edit_contract/<int:pk>/", views.edit_contract, name="edit_contract"),
    path("add_contract/<int:pk>/", views.add_contract, name="add_contract"),
    path(
        "delete_contract_file/<int:pk>/",
        views.delete_contract_file,
        name="delete_contract_file",
    ),
    #### HTMX URLS ####
    path("create_invoice_form/", views.create_invoice_form, name="create_invoice_form"),
    path("vendor_contracts/", views.vendor_contracts, name="vendor_contracts"),
    path(
        "invoice_for_contract/", views.invoice_for_contract, name="invoice_for_contract"
    ),
    path("invoice_history/<int:pk>/", views.invoice_history, name="invoice_history"),
]