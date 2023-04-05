"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from app import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),

    path("",views.login,name="login"),
    path("logout",views.logout,name="logout"),

    path("home",views.home,name="home"),
    path("new-building-form",views.building_form,name="building-form"),
    path("delete-building/<int:id>",views.delete_building,name="delete-building"),

    path("apartments/<int:id>",views.apartments,name="apartments"),
    path("new-apartment-form/<int:id>",views.apartment_form,name="apartment-form"),
    path("edit-apartment-form/<int:id>",views.edit_apartment_form,name="edit-apartment-form"),
    path("delete-apartment/<int:id>",views.delete_apartment,name="delete-apartment"),

    path("invoices/<int:id>",views.invoices,name="invoices"),
    path("new-invoice-form/<int:id>",views.invoice_form,name="invoice-form"),

    path("print-invoice/<int:id>",views.print_invoice,name="print-invoice"),
    path("delete-invoice/<int:id>",views.delete_invoice,name="delete-invoice"),

    path("owner-invoices/<str:id>",views.owner_invoices,name="owner-invoices"),

    path("maintenance-invoices/<int:id>",views.maintenance_invoices,name="maintenance-invoices"),
    path("new-maintenance-invoice-form/<int:id>",views.maintenance_invoice_form,name="maintenance-invoice-form"),
    path("delete-maintenance-invoice/<int:id>",views.delete_maintenance_invoice,name="delete-maintenance-invoice"),
    path("owner-maintenance-invoices/<str:id>",views.owner_maintenance_invoices,name="owner-maintenance-invoices"),

    path("owner-report/<str:id>",views.owner_report,name="owner-report"),

]
