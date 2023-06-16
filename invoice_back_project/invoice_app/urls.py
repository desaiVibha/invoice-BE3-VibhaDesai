from django.urls import path
from .views import UserSignUp,GetAllInvoices,NewInvoice,GetInvoiceByID,AddItem
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('signup/',csrf_exempt(UserSignUp.as_view()),name='sign-up'),
    path('invoices/',csrf_exempt(GetAllInvoices.as_view()),name='get-all-invoices'),
    path('invoices/new',csrf_exempt(NewInvoice.as_view()),name='new-invoice'),
    path('invoices/<int:id>',csrf_exempt(GetInvoiceByID.as_view()),name='get-invoice-by-id'),
    path('invoices/<int:id>/items',csrf_exempt(AddItem.as_view()),name='add-item')
]