from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView 
from vMac.models import *
from vMac.serializer import *
import uuid
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# from rest_framework import 
# Create your views here.

class vendorViews(APIView):
    def get(self,request,id=""):
        if id=="":
            vendors = Vendor.objects.all()
        else:
            vendors = Vendor.objects.filter(vendor_code=id)
            if len(vendors) == 0:
                return Response({"Error":"Invalid id"},status=404)
            
        vendor_serializer = VendorSerializer(vendors, many=True)
        return Response({"status":200, "Payload":vendor_serializer.data},status=200)

    def post(self,request,*args,**kwargs):
        if len(kwargs)>0:
            return Response({"Status":"Failed","Error":"Wrong end point for post data"},status=400)
        data = request.data

        if "vendor_code" in data:
            return Response({"Status":"Failed","Error":"Please Dont pass vendor code its an autofield uniquelly"}, status=400)
        
        vCode = str(uuid.uuid4())[0:7]
        data["vendor_code"] = vCode

        Vserializer = VendorSerializer(data=data)

        if Vserializer.is_valid():
            Vserializer.save()
            return Response({"Status":"Success", "Message":f"Vendor Added Successfully with vendor code = {vCode}"}, status=200)
        else:
            return Response({"Status":"Failed","Error":str(Vserializer.errors)}, status=400)
        
    def put(self,request,id):

        try: 
            vendors = Vendor.objects.get(vendor_code=id)
        
            vserializer = VendorSerializer(vendors, data = request.data, partial=True)

            if vserializer.is_valid() :
                vserializer.save()
                return Response({"Status":"Successful","Payload":vserializer.data, "Message":"Vendor Updated Successfully!"})
            return Response({"Status":"Failed","Error":"Bad Request"}, status=400)

        except Exception as e:
            return Response({"Status":"Failed","Error":f"{e}"}, status=400)


    def delete(self,request,id):
        try:
            obj = Vendor.objects.get(vendor_code=id).delete()
            return Response({"Status":"success","Message":"Vendor deleted SuccesFully"},status=200)
        
        except Exception as e:
            return Response({"Status":"Failed","Message":f"{e}"},status=400)


class PoViews(APIView):
    
    def get(self,request,id=""):
        if id=="":
            pos = Po.objects.all()
        else:
            pos = Po.objects.filter(po_number=id)
            if len(pos) == 0:
                return Response({"Error":"Invalid Order number"},status=404)
            
        po_serializer = PoSerializer(pos, many=True)
        return Response({"status":200, "Payload":po_serializer.data},status=200)

    def post(self,request,*args,**kwargs):
        if len(kwargs)>0:
            return Response({"Status":"Failed","Error":"Wrong end point for post data"},status=400)
        data = request.data
        if "po_number" in data:
            return Response({"Status":"Failed","Error":"Please Dont pass vendor code its an autofield uniquelly"}, status=400)
        ponum = str(uuid.uuid4())[:25]
        data["po_number"] = ponum
        Poserializer = PoSerializer(data=data)

        if Poserializer.is_valid():
            Poserializer.save()
            return Response({"Status":"Success", "Message":f"Order Added Successfully with Order Number = {ponum}"}, status=200)
        else:
            return Response({"Status":"Failed","Error":str(Poserializer.errors)}, status=400)
        
    def put(self,request,id):

        try: 
            pos = Po.objects.get(po_number=id)
        
            Poserializer = PoSerializer(pos, data = request.data, partial=True)

            if Poserializer.is_valid() :
                Poserializer.save()
                return Response({"Status":"Successful","Payload":Poserializer.data, "Message":"order Updated Successfully!"})
            return Response({"Status":"Failed","Error":"Bad Request"}, status=400)

        except Exception as e:
            
            return Response({"Status":"Failed","Error":f"{e}"}, status=400)


    def delete(self,request,id):
        try:
            obj = Po.objects.get(po_number=id).delete()
            return Response({"Status":"success","Message":"order deleted SuccesFully"},status=200)
        
        except Exception as e:
            return Response({"Status":"Failed","Message":f"{e}"},status=400)


class Performance(APIView):

    def get(self,request,id):
        try:
            vendor = Vendor.objects.get(vendor_code = id)
            performance = HistoricalPerformance.objects.get(vendor=vendor)
            PerfoSerializer = PerformSerializer(performance)
            vendorSeializer = VendorSerializer(vendor)
            return Response({"Status":"Sucess","Vendor":vendorSeializer.data,"Performances":PerfoSerializer.data},status=200)


        except Exception as e:
            return Response({"Status":"Failed","Message":f"{e}"},status=400)


