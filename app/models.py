from django.db import models
from django.contrib.auth.models import User
import uuid

class building(models.Model):
    name = models.CharField(max_length=300,null=True,blank=True)
    invoice_owner = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.name

class apartment(models.Model):
    aprt_number = models.CharField(max_length=50,null=True,blank=True)
    name = models.CharField(max_length=300,null=True,blank=True)
    phone_nmber = models.CharField(max_length=50,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    contract_number = models.CharField(max_length=300,null=True,blank=True)
    elect_number = models.CharField(max_length=300,null=True,blank=True)
    note = models.TextField(max_length=2000,null=True,blank=True)
    building = models.ForeignKey(building,on_delete=models.CASCADE)

    def __str__(self):
        return self.building.name + " - " + self.aprt_number

class invoice(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apartment = models.ForeignKey(apartment,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=100,null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    today_date = models.DateField(auto_now_add=True)
    remaining_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.apartment.building.name + " - " + self.apartment.aprt_number + " - {}".format(self.unique_id)