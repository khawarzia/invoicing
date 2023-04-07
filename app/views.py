from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .models import *
from PyPDF2 import PdfFileWriter, PdfFileReader
import arabic_reshaper
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import openpyxl
import datetime

def get_user_profile(userobj):
    try:
        obj = user_profile.objects.get(user=userobj)
    except:
        obj = user_profile()
        obj.user = userobj
        obj.save()
    return obj

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
    obj = get_user_profile(request.user)
    context['type_of_user'] = obj.type_of_user == 'd'
    if obj.type_of_user == 'v':
        temp = building.objects.all()
        temp2 = invoice_owner.objects.all()
        temp_list = []
        temp2_list = []
        for i in temp:
            if i.owner in obj.invoice_owner_allowed.all():
                temp_list.append(i)
        for i in temp2:
            if i in obj.invoice_owner_allowed.all():
                temp2_list.append(i)
        context['objs'] = temp_list
        context['owners'] = temp2_list
    else:
        context['objs'] = building.objects.all()
        context['owners'] = invoice_owner.objects.all()
    return render(request,template,context)

@login_required(login_url='/')
def delete_building(request,id):
    obj = building.objects.get(pk=id)
    obj.delete()
    return redirect("/home")
    
@login_required(login_url='/')
def building_form(request):
    template = "new_building_form.html"
    context = {}
    context['objs'] = invoice_owner.objects.all()
    if request.method == "POST":
        if request.POST['name'] and request.POST['invoice-owner']:
            objs = building.objects.filter(name=request.POST['name'])
            if len(objs) == 0:
                obj = building()
                obj.name = request.POST['name']
                obj.owner = invoice_owner.objects.get(pk=request.POST['invoice-owner'])
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
        obj = get_user_profile(request.user)
        context['type_of_user'] = obj.type_of_user == 'd'
        building_obj = building.objects.get(pk=id)
        objs = apartment.objects.filter(building=building_obj)
        context['bobj'] = building_obj
        context['objs'] = objs
        if context['type_of_user']:
            context['owners'] = invoice_owner.objects.all()
        else:
            temp2 = invoice_owner.objects.all()
            temp2_list = []
            for i in temp2:
                if i in obj.invoice_owner_allowed.all():
                    temp2_list.append(i)
            context['owners'] = temp2_list
        if request.method == "POST":
            if request.POST['name'] and request.POST['invoice-owner']:
                objs = building.objects.filter(name=request.POST['name'])
                if (len(objs) == 0 and building_obj.name != request.POST['name']) or (len(objs) == 1 and building_obj.name == request.POST['name']):
                    building_obj.name = request.POST['name']
                    building_obj.owner = invoice_owner.objects.get(pk=request.POST['invoice-owner'])
                    building_obj.save()
                    return redirect("/apartments/{}".format(id))
                else:
                    context['message'] = "Building with that name already exists."
            else:
                context['message'] = "Entered data is not valid."
        return render(request,template,context)
    else:
        return redirect('/home')

@login_required(login_url='/')
def apartment_form(request,id):
    if id:
        template = "new_apartment_form.html"
        context = {'id':id}
        if request.method == "POST":
            if request.POST['name'] and request.POST['num'] and request.POST['phone'] and request.POST['type_of'] and request.POST['dob'] and request.POST['cnum'] and request.POST['enum']:
                bobj = building.objects.get(pk=id)
                objs = apartment.objects.filter(aprt_number=request.POST['num'],building=bobj)
                if len(objs) == 0:
                    obj = apartment()
                    obj.aprt_number = request.POST['num']
                    obj.name = request.POST['name']
                    obj.type_of = request.POST['type_of']
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
def edit_apartment_form(request,id):
    if id:
        template = "apartments_invoice.html"
        context = {}
        if request.method == "POST":
            if request.POST['name'] and request.POST['num'] and request.POST['phone'] and request.POST['type_of'] and request.POST['dob'] and request.POST['cnum'] and request.POST['enum']:
                objs = apartment.objects.filter(pk=id)
                if len(objs) == 1 and len(apartment.objects.filter(building=objs[0].building, aprt_number=request.POST['num'])) == 1:
                    obj = objs[0]
                    obj.aprt_number = request.POST['num']
                    obj.name = request.POST['name']
                    obj.type_of = request.POST['type_of']
                    obj.dob = request.POST['dob']
                    obj.phone_nmber = request.POST['phone']
                    obj.elect_number = request.POST['enum']
                    obj.contract_number = request.POST['cnum']
                    obj.note = request.POST['note']
                    obj.save()
                    return redirect("/invoices/{}".format(id))
                else:
                    context['message'] = "Apartment with that number already exists in this building."
            else:
                context['message'] = "Entered data is not valid."
        obj = apartment.objects.filter(pk=id)[0]
        objs = invoice.objects.filter(apartment=obj)
        context['aobj'] = obj
        context['objs'] = objs
        return render(request,template,context)
    else:
        return redirect("/home")

@login_required(login_url='/')
def delete_apartment(request,id):
    if id:
        obj = apartment.objects.filter(pk=id)[0]
        bid = obj.building.id
        obj.delete()
        return redirect("/apartments/{}".format(bid))
    else:
        return redirect("/home")

@login_required(login_url='/')
def invoices(request,id):
    if id:
        template = "apartments_invoice.html"
        context = {}
        obj = get_user_profile(request.user)
        context['type_of_user'] = obj.type_of_user == 'd'
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
        context['date_dis'] = aobj.dob.strftime("%Y-%m-%d")
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
            if request.POST['amount'] and (request.POST['payment'] == "Cash" or (request.POST['payment'] == "Transfer" and request.POST['bank'] and request.POST['trans_date'])) and request.POST['fdate'] and request.POST['tdate']:
                obj = invoice()
                obj.user = request.user
                obj.apartment = apartment.objects.get(pk=id)
                obj.owner = apartment.objects.get(pk=id).building.owner
                obj.amount = request.POST['amount']
                if request.POST['ramount']:
                    obj.remaining_amount = request.POST['ramount']
                else:
                    obj.remaining_amount = 0
                obj.payment_method = request.POST['payment']
                if (request.POST['payment'] == "Transfer"):
                    obj.bank_of_transfer = request.POST['bank']
                    obj.transfer_date = request.POST['trans_date']
                obj.from_date = request.POST['fdate']
                obj.to_date = request.POST['tdate']
                if request.POST['note']:
                    obj.note = request.POST['note']
                obj.save()
                return redirect("/invoices/{}".format(id))
            else:
                context['message'] = "Entered data is not valid."
        return render(request,template,context)
    else:
        return redirect("/home")

def get_reversed(a):
    retval = ""
    for i in range(1,len(a)):
        retval += a[len(a)-i]
    retval += a[0]
    return retval

@login_required(login_url='/')
def print_invoice(request,id):

    pdfmetrics.registerFont(TTFont("Arabic","font.ttf"))

    obj = invoice.objects.filter(pk=id)

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)
    p.setFont('Arabic', 15)
    
    if (len(obj) == 1):
        p.drawString(225, 660, "{}".format(obj[0].today_date.strftime("%d-%m-%Y")))

        p.drawString(250, 630, "{:05d}".format(id))

        p.drawString(320, 512, "{}".format(obj[0].amount))

        p.drawString(120, 536, get_display(arabic_reshaper.reshape(obj[0].apartment.name)) )

        p.drawString(120, 482, obj[0].apartment.contract_number)

        if (obj[0].payment_method == "Cash"):
            p.drawString(484, 447.5, "X")
        else:
            p.drawString(433, 447.5, "X")
            p.drawString(80, 447.5, "{}".format(obj[0].transfer_date.strftime("%d-%m-%Y")))
            p.drawString(225, 447.5, get_display(arabic_reshaper.reshape(obj[0].bank_of_transfer)))

        p.drawString(360, 418, "{}".format(obj[0].apartment.type_of))

        p.drawString(295, 418, "{}".format(obj[0].apartment.aprt_number))

        p.drawString(98, 418, "{}".format(get_display(arabic_reshaper.reshape(obj[0].apartment.building.name))))

        p.drawString(370, 393, "{}".format(obj[0].from_date.strftime("%d-%m-%Y")))

        p.drawString(80, 393, "{}".format(obj[0].to_date.strftime("%d-%m-%Y")))

        p.drawString(380, 190, obj[0].user.username)

        p.drawString(65,333, "{} {} : Remaining Amount".format(get_display(arabic_reshaper.reshape("ريال فقط لاغير")),obj[0].remaining_amount))

        p.setFont('Arabic', 13)

        p.drawString(65,305, get_display(arabic_reshaper.reshape(obj[0].note)))

    p.showPage()
    p.save()

    buffer.seek(0)

    new_pdf = PdfFileReader(buffer)

    existing_pdf = PdfFileReader("RealEstateInvoiceCom.pdf")
    output = PdfFileWriter()

    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    outputStream = io.BytesIO()
    output.write(outputStream)
    outputStream.seek(0)

    return FileResponse(outputStream , as_attachment=True, filename='invoice.pdf')

@login_required(login_url='/')
def delete_invoice(request,id):
    obj = invoice.objects.get(pk=id)
    try:
        tempId = obj.apartment.id
        obj.delete()
        return redirect("/invoices/{}".format(tempId))
    except:
        obj.delete()
        return redirect('/home')

@login_required(login_url='/')
def owner_invoices(request,id):
    if id:
        template = "owners_invoice.html"
        context = {}
        obj = get_user_profile(request.user)
        context['type_of_user'] = obj.type_of_user == 'd'
        if id != "x":
            context['sel_owner'] = int(id)
        if request.method == "POST" and request.POST['asc_desc'] in ("0","1"):
            context["order"] = request.POST['asc_desc']
            if request.POST["asc_desc"] == "0":
                if id != "x":
                    objs = invoice.objects.filter(owner__id=int(id)).order_by("today_date")
                else:
                    if obj.type_of_user == 'v':
                        temp2 = invoice.objects.all().order_by("today_date")
                        objs = []
                        for i in temp2:
                            if i.owner in obj.invoice_owner_allowed.all():
                                objs.append(i)
                    else:
                        objs = invoice.objects.all().order_by("today_date")
            else:
                if id != "x":
                    objs = invoice.objects.filter(owner__id=int(id)).order_by("-today_date")
                else:
                    if obj.type_of_user == 'v':
                        temp2 = invoice.objects.all().order_by("-today_date")
                        objs = []
                        for i in temp2:
                            if i.owner in obj.invoice_owner_allowed.all():
                                objs.append(i)
                    else:
                        objs = invoice.objects.all().order_by("-today_date")
        else:
            if id != "x":
                objs = invoice.objects.filter(owner__id=int(id))
            else:
                if obj.type_of_user == 'v':
                    temp2 = invoice.objects.all()
                    objs = []
                    for i in temp2:
                        if i.owner in obj.invoice_owner_allowed.all():
                            objs.append(i)
                else:
                    objs = invoice.objects.all()

        context['objs'] = objs
        if obj.type_of_user == 'v':
            temp2 = invoice_owner.objects.all()
            temp2_list = []
            for i in temp2:
                if i in obj.invoice_owner_allowed.all():
                    temp2_list.append(i)
            context['owners'] = temp2_list
        else:
            context['owners'] = invoice_owner.objects.all()
        return render(request,template,context)
    else:
        return redirect('/home')
    



@login_required(login_url='/')
def maintenance_invoices(request,id):
    if id:
        template = "apartments_maintenance_invoice.html"
        context = {}
        obj = get_user_profile(request.user)
        context['type_of_user'] = obj.type_of_user == 'd'
        aobj = apartment.objects.get(pk=id)
        if request.method == "POST" and request.POST['asc_desc'] in ("0","1"):
            context["order"] = request.POST['asc_desc']
            if request.POST["asc_desc"] == "0":
                objs = maintenance_invoice.objects.filter(apartment=aobj).order_by("today_date")
            else:
                objs = maintenance_invoice.objects.filter(apartment=aobj).order_by("-today_date")
        else:
            objs = maintenance_invoice.objects.filter(apartment=aobj)
        context['aobj'] = aobj
        context['date_dis'] = aobj.dob.strftime("%Y-%m-%d")
        context['objs'] = objs
        return render(request,template,context)
    else:
        return redirect('/home')

@login_required(login_url='/')
def maintenance_invoice_form(request,id):
    if id:
        template = "new_maintenance_invoice_form.html"
        context = {'id':id}
        if request.method == "POST":
            if request.POST['amount']:
                obj = maintenance_invoice()
                obj.user = request.user
                obj.apartment = apartment.objects.get(pk=id)
                obj.owner = apartment.objects.get(pk=id).building.owner
                obj.amount = request.POST['amount']
                if request.POST['note']:
                    obj.note = request.POST['note']
                obj.save()
                return redirect("/maintenance-invoices/{}".format(id))
            else:
                context['message'] = "Entered data is not valid."
        return render(request,template,context)
    else:
        return redirect("/home")
    
@login_required(login_url='/')
def delete_maintenance_invoice(request,id):
    obj = maintenance_invoice.objects.get(pk=id)
    try:
        tempId = obj.apartment.id
        obj.delete()
        return redirect("/invoices/{}".format(tempId))
    except:
        obj.delete()
        return redirect('/home')

@login_required(login_url='/')
def owner_maintenance_invoices(request,id):
    if id:
        template = "owners_maintenance_invoice.html"
        context = {}
        obj = get_user_profile(request.user)
        context['type_of_user'] = obj.type_of_user == 'd'
        if id != "x":
            context['sel_owner'] = int(id)
        if request.method == "POST" and request.POST['asc_desc'] in ("0","1"):
            context["order"] = request.POST['asc_desc']
            if request.POST["asc_desc"] == "0":
                if id != "x":
                    objs = invoice.objects.filter(owner__id=int(id)).order_by("today_date")
                else:
                    if obj.type_of_user == 'v':
                        temp2 = invoice.objects.all().order_by("today_date")
                        objs = []
                        for i in temp2:
                            if i.owner in obj.invoice_owner_allowed.all():
                                objs.append(i)
                    else:
                        objs = invoice.objects.all().order_by("today_date")
            else:
                if id != "x":
                    objs = invoice.objects.filter(owner__id=int(id)).order_by("-today_date")
                else:
                    if obj.type_of_user == 'v':
                        temp2 = invoice.objects.all().order_by("-today_date")
                        objs = []
                        for i in temp2:
                            if i.owner in obj.invoice_owner_allowed.all():
                                objs.append(i)
                    else:
                        objs = invoice.objects.all().order_by("-today_date")
        else:
            if id != "x":
                objs = invoice.objects.filter(owner__id=int(id))
            else:
                if obj.type_of_user == 'v':
                    temp2 = invoice.objects.all()
                    objs = []
                    for i in temp2:
                        if i.owner in obj.invoice_owner_allowed.all():
                            objs.append(i)
                else:
                    objs = invoice.objects.all()

        context['objs'] = objs
        if obj.type_of_user == 'v':
            temp2 = invoice_owner.objects.all()
            temp2_list = []
            for i in temp2:
                if i in obj.invoice_owner_allowed.all():
                    temp2_list.append(i)
            context['owners'] = temp2_list
        else:
            context['owners'] = invoice_owner.objects.all()
        return render(request,template,context)
    else:
        return redirect('/home')

def owner_report(request,id):
    date_col_rows = [{'row_start':4,'row_end':19,'col_start':10,'col_end':16},{'row_start':4,'row_end':19,'col_start':2,'col_end':8}]
    date_col_rows_inv = [{'row_start':4,'row_end':19,'col_start':10,'col_end':14},{'row_start':4,'row_end':19,'col_start':2,'col_end':6}]
    date_col_rows_main = [{'row_start':4,'row_end':19,'col_start':15,'col_end':16},{'row_start':4,'row_end':19,'col_start':7,'col_end':8}]
    row_offset = 21
    workbook = openpyxl.load_workbook('Monthly_report.xlsx')
    worksheet = workbook.get_sheet_by_name(workbook.get_sheet_names()[0])

    sel_date = datetime.datetime.now()

    owner_obj = invoice_owner.objects.get(pk=id)
    invoice_objs = invoice.objects.filter(owner=owner_obj,today_date__month=sel_date.month,today_date__year=sel_date.year).order_by("today_date")
    maintenance_objs = maintenance_invoice.objects.filter(owner=owner_obj,today_date__month=sel_date.month,today_date__year=sel_date.year).order_by("today_date")

    offset = 0
    for i in range(1,32):
        limits = date_col_rows[i%2]
        for r in range(limits['row_start']+offset,limits['row_end']+1+offset):
            for c in range(limits['col_start'],limits['col_end']+1):
                cell = worksheet.cell(row=r,column=c)
                cell.value = ""
        
        inv_data = []
        for j in invoice_objs:
            if j.today_date.day == i:
                inv_data.append(j)

        limits = date_col_rows_inv[i%2]
        for j,r in zip(inv_data,range(limits['row_start']+offset,limits['row_end']+1+offset)):
            cell = worksheet.cell(row=r,column=limits['col_start'])
            cell.value = j.apartment.aprt_number
            cell = worksheet.cell(row=r,column=limits['col_start']+1)
            cell.value = j.apartment.building.name
            if j.payment_method == 'Cash':
                cell = worksheet.cell(row=r,column=limits['col_start']+2)
                cell.value = j.amount
            else:
                cell = worksheet.cell(row=r,column=limits['col_start']+3)
                cell.value = j.amount
            cell = worksheet.cell(row=r,column=limits['col_start']+4)
            cell.value = j.id

        main_data = []
        for j in maintenance_objs:
            if j.today_date.day == i:
                main_data.append(j)

        limits = date_col_rows_main[i%2]
        for j,r in zip(main_data,range(limits['row_start']+offset,limits['row_end']+1+offset)):
            cell = worksheet.cell(row=r,column=limits['col_start'])
            cell.value = j.amount
            cell = worksheet.cell(row=r,column=limits['col_start']+1)
            cell.value = j.note

        
        if (i % 2 == 0):
            offset += row_offset





    workbook.save('Monthly_report.xlsx')

    return FileResponse(open("Monthly_report.xlsx","rb"), as_attachment=True)