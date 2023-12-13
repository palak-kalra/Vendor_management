from django.db import models
import datetime
# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=7,primary_key=True)
    

    def __str__(self):
        return f"{self.name}__{self.vendor_code}"
    

class Po(models.Model):
    choices = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Canceled','Canceled')
    )
    po_number = models.CharField(max_length=30, unique=True,primary_key=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=datetime.datetime.today())
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20,choices=choices)
    quality_rating = models.FloatField(null=True,blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True,blank=True)
    delivered_at_time = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.po_number}"

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.today())
    on_time_delivery_rate = models.FloatField(max_length=5,default=0)
    quality_rating_avg = models.FloatField(max_length=5,default=0)
    average_response_time = models.FloatField(max_length=5,default=0)
    fulfillment_rate = models.FloatField(max_length=5,default=0)

    def __str__(self):
        return f"vendor '{self.vendor.name}' Performance"


    

    