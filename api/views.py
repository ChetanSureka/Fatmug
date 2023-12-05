from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from django.utils import timezone

class VendorListCreateAPIView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetailAPIView(APIView):
    def get_object(self, vendor_id):
        try:
            return Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseOrderListCreateAPIView(APIView):
    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderDetailAPIView(APIView):
    def get_object(self, po_id):
        try:
            return PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, po_id):
        po = self.get_object(po_id)
        serializer = PurchaseOrderSerializer(po)
        return Response(serializer.data)

    def put(self, request, po_id):
        po = self.get_object(po_id)
        serializer = PurchaseOrderSerializer(po, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id):
        po = self.get_object(po_id)
        po.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorPerformanceAPIView(APIView):
    def get_object(self, vendor_id):
        try:
            return Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_data)

class AcknowledgePurchaseOrderAPIView(APIView):
    def get_object(self, po_id):
        try:
            return PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def post(self, request, po_id):
        po = self.get_object(po_id)
        po.acknowledgment_date = timezone.now()
        po.save()

        # Trigger recalculation of average_response_time (implement the logic here)

        return Response({'acknowledgment_date': po.acknowledgment_date})
