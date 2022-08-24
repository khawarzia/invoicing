from datetime import date
from statistics import mode
from django.db import models
from django.contrib.auth.models import User

class invoice_owner(models.Model):
    name = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.name
    
class building(models.Model):
    name = models.CharField(max_length=300,null=True,blank=True)
    owner = models.ForeignKey(invoice_owner,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.name

class apartment(models.Model):
    aprt_number = models.CharField(max_length=50,null=True,blank=True)
    name = models.CharField(max_length=300,null=True,blank=True)
    phone_nmber = models.CharField(max_length=50,null=True,blank=True)
    type_of = models.CharField(max_length=300,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    contract_number = models.CharField(max_length=300,null=True,blank=True)
    elect_number = models.CharField(max_length=300,null=True,blank=True)
    note = models.TextField(max_length=2000,null=True,blank=True)
    building = models.ForeignKey(building,on_delete=models.CASCADE)

    def __str__(self):
        return self.building.name + " - " + self.aprt_number

    def getShowColor(self):
        invs = invoice.objects.filter(apartment=self).order_by("today_date")
        if (len(invs) == 0):
            return "green"
        inv = invs[len(invs) - 1]
        comp_date = date.today()
        to_date = date(inv.to_date.year,inv.to_date.month,inv.to_date.day)
        if (to_date >= comp_date):
            return "green"
        else:
            comp = comp_date - to_date
            if (comp.days <= 30):
                return "yellow"
            elif (comp.days > 30 and comp.days <= 90):
                return "red"
            else:
                return "black"

class invoice(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    apartment = models.ForeignKey(apartment,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=100,null=True,blank=True)
    bank_of_transfer = models.CharField(max_length=300,null=True,blank=True)
    transfer_date = models.DateField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    today_date = models.DateField(auto_now_add=True)
    remaining_amount = models.IntegerField(default=0)
    note = models.TextField(max_length=2000,null=True,blank=True)

    def __str__(self):
        return self.apartment.building.name + " - " + self.apartment.aprt_number + " - {}".format(self.unique_id)