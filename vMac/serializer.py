from rest_framework import serializers
from vMac.models import *
import datetime

class PerformSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        # fields = "__all__" 
        exclude = ["id"]




class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__" 

    def create(self, validated_data):
        x = super().create(validated_data)
        data = {"vendor":validated_data["vendor_code"]}
        PS = PerformSerializer(data=data)

        if PS.is_valid():
            PS.save()
        else:
            print(PS.errors)

        return x



class PoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Po
        fields = "__all__" 


    def update(self, instance, validated_data):

        order = Po.objects.get(po_number = instance)
        if validated_data['status'] == "Completed":
            if (datetime.date.today() <= order.delivery_date.date()):
                validated_data["delivered_at_time"] = True


        if validated_data["status"] != order.status:
            vendor = Vendor.objects.get(vendor_code = order.vendor.vendor_code)
            orders = Po.objects.filter(vendor = vendor)
            orders_completed = Po.objects.filter(vendor = vendor, status = "Completed", delivered_at_time = True)

            fullfill = len(orders_completed)/len(orders)

            performance_matrix = HistoricalPerformance.objects.get(vendor = vendor)

            performance_matrix.fulfillment_rate = fullfill
            performance_matrix.save()


        updated = super().update(instance, validated_data)


        if validated_data['status'] == "Completed":
            # print(order.vendor.vendor_code)
            vendor = Vendor.objects.get(vendor_code = order.vendor.vendor_code)
            orders = Po.objects.filter(vendor = vendor)
            orders_completed = Po.objects.filter(vendor = vendor, status = "Completed",delivered_at_time = True)
            total_orders = len(orders)
            total_orders_completed_on_time = len(orders_completed)

            on_time_delivery_rate_cal = total_orders_completed_on_time/total_orders

            performance_matrix = HistoricalPerformance.objects.get(vendor = vendor)

            performance_matrix.on_time_delivery_rate = on_time_delivery_rate_cal
            performance_matrix.save()


        if validated_data['quality_rating'] is not None:
            vendor = Vendor.objects.get(vendor_code = order.vendor.vendor_code)
            orders = Po.objects.filter(vendor = vendor,status="Completed")

            total_order = 0
            temp = 0

            for i in orders:
                total_order += 1
                temp += i.quality_rating
            
            avrg_qual_rat = temp/total_order

            performance_matrix = HistoricalPerformance.objects.get(vendor = vendor)

            performance_matrix.quality_rating_avg = avrg_qual_rat
            performance_matrix.save()


        
        if validated_data['acknowledgment_date'] is not None:
            vendor = Vendor.objects.get(vendor_code = order.vendor.vendor_code)
            response_time = order.acknowledgment_date.date() - order.issue_date.date()

            performance_matrix = HistoricalPerformance.objects.get(vendor = vendor)

            x = performance_matrix.average_response_time
            performance_matrix.average_response_time = (x+response_time)/2

            performance_matrix.save()






        return updated




