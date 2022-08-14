from enum import unique
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .models import *
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

def login(request):
    if request.user.is_authenticated:
        return redirect("/home")
    template = "login.html"
    context = {}
    if request.method == "POST":
        user = User.objects.filter(username=request.POST['user'])
        if (len(user) > 0):
            user = user[0]
            if (user.check_password(request.POST['pass'])):
                auth.login(request,user)
                return redirect("/home")
            else:
                context['message'] = "The entered password is not correct!"
        else:
            context['message'] = "The entered user was not found!"
    return render(request,template,context)

def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required(login_url='/')
def home(request):
    template = "home.html"
    context = {}
    context['objs'] = building.objects.all()
    return render(request,template,context)
    
@login_required(login_url='/')
def building_form(request):
    template = "new_building_form.html"
    context = {}
    if request.method == "POST":
        if request.POST['name'] and request.POST['invoice-owner']:
            objs = building.objects.filter(name=request.POST['name'])
            if len(objs) == 0:
                obj = building()
                obj.name = request.POST['name']
                obj.invoice_owner = request.POST['invoice-owner']
                obj.save()
                return redirect('/home')
            else:
                context['message'] = "Building with that name already exists."
        else:
            context['message'] = "Entered data is not valid."
    return render(request,template,context)

@login_required(login_url='/')
def apartments(request,id):
    if id:
        template = "apartments.html"
        context = {}
        building_obj = building.objects.get(pk=id)
        objs = apartment.objects.filter(building=building_obj)
        context['bobj'] = building_obj
        context['objs'] = objs
        return render(request,template,context)
    else:
        return redirect('/home')

@login_required(login_url='/')
def apartment_form(request,id):
    if id:
        template = "new_apartment_form.html"
        context = {'id':id}
        if request.method == "POST":
            if request.POST['name'] and request.POST['num'] and request.POST['phone'] and request.POST['dob'] and request.POST['cnum'] and request.POST['enum']:
                bobj = building.objects.get(pk=id)
                objs = apartment.objects.filter(aprt_number=request.POST['num'],building=bobj)
                if len(objs) == 0:
                    obj = apartment()
                    obj.aprt_number = request.POST['num']
                    obj.name = request.POST['name']
                    obj.dob = request.POST['dob']
                    obj.phone_nmber = request.POST['phone']
                    obj.elect_number = request.POST['enum']
                    obj.contract_number = request.POST['cnum']
                    obj.note = request.POST['note']
                    obj.building = bobj
                    obj.save()
                    return redirect("/apartments/{}".format(id))
                else:
                    context['message'] = "Apartment with that number already exists in this building."
            else:
                context['message'] = "Entered data is not valid."
        return render(request,template,context)
    else:
        return redirect("/home")

@login_required(login_url='/')
def invoices(request,id):
    if id:
        template = "apartments_invoice.html"
        context = {}
        aobj = apartment.objects.get(pk=id)
        if request.method == "POST" and request.POST['asc_desc'] in ("0","1"):
            context["order"] = request.POST['asc_desc']
            if request.POST["asc_desc"] == "0":
                objs = invoice.objects.filter(apartment=aobj).order_by("today_date")
            else:
                objs = invoice.objects.filter(apartment=aobj).order_by("-today_date")
        else:
            objs = invoice.objects.filter(apartment=aobj)
        context['aobj'] = aobj
        context['objs'] = objs
        return render(request,template,context)
    else:
        return redirect('/home')

@login_required(login_url='/')
def invoice_form(request,id):
    if id:
        template = "new_invoice_form.html"
        context = {'id':id}
        if request.method == "POST":
            if request.POST['amount'] and request.POST['ramount'] and request.POST['payment'] and request.POST['fdate'] and request.POST['tdate']:
                obj = invoice()
                obj.user = request.user
                obj.apartment = apartment.objects.get(pk=id)
                obj.amount = request.POST['amount']
                obj.remaining_amount = request.POST['ramount']
                obj.payment_method = request.POST['payment']
                obj.from_date = request.POST['fdate']
                obj.to_date = request.POST['tdate']
                obj.save()
                return redirect("/invoices/{}".format(id))
            else:
                context['message'] = "Entered data is not valid."
        return render(request,template,context)
    else:
        return redirect("/home")

@login_required(login_url='/')
def print_invoice(request,id):

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)

    obj = invoice.objects.filter(unique_id=id)
    if (len(obj) == 1):

        p.drawString(295, 580, "{}".format(obj[0].today_date))

        p.drawString(238, 543, "{}".format(id))

        p.drawString(321, 526, "{}".format(obj[0].amount))

        p.drawString(118, 483, obj[0].apartment.name)

        p.drawString(180, 450, obj[0].apartment.phone_nmber)

        p.drawString(200, 415, "{}".format(obj[0].remaining_amount))

        p.drawString(110, 380, "{}".format(obj[0].from_date))

        p.drawString(340, 380, "{}".format(obj[0].to_date))

        p.drawString(420, 250, obj[0].user.username)

    p.showPage()
    p.save()

    buffer.seek(0)

    new_pdf = PdfFileReader(buffer)

    existing_pdf = PdfFileReader("testpdf.pdf")
    output = PdfFileWriter()

    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    outputStream = io.BytesIO()
    output.write(outputStream)
    outputStream.seek(0)
    #outputStream.close()

    return FileResponse(outputStream , as_attachment=True, filename='invoice.pdf')