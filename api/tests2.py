from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder

class VendorAPITestCase(TestCase):
    '''
        These test cases cover:

        Creating a vendor (test_vendor_list_create_api).
        Retrieving a specific vendor (test_vendor_detail_api).
        Retrieving vendor performance metrics (test_vendor_performance_api).
        Updating a vendor (test_vendor_update_api).
        Deleting a vendor (test_vendor_delete_api).
    '''
    def setUp(self):
        self.client = APIClient()

    def test_vendor_list_create_api(self):
        # Test creating a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor A', 'contact_details': 'Contact A', 'address': 'Address A', 'vendor_code': 'VENDOR001'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)

        # Test listing vendors
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_vendor_detail_api(self):
        # Create a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor B', 'contact_details': 'Contact B', 'address': 'Address B', 'vendor_code': 'VENDOR002'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Test retrieving a specific vendor
        response = self.client.get(f'/api/vendors/{vendor_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Vendor B')

    def test_vendor_performance_api(self):
        # Create a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor C', 'contact_details': 'Contact C', 'address': 'Address C', 'vendor_code': 'VENDOR003'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Test retrieving vendor performance metrics
        response = self.client.get(f'/api/vendors/{vendor_id}/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_update_api(self):
        # Create a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor D', 'contact_details': 'Contact D', 'address': 'Address D', 'vendor_code': 'VENDOR004'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Update the vendor
        updated_data = {'name': 'Updated Vendor D', 'contact_details': 'Updated Contact D', 'address': 'Updated Address D', 'vendor_code': 'VENDOR004'}
        response = self.client.put(f'/api/vendors/{vendor_id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Vendor D')

    def test_vendor_delete_api(self):
        # Create a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor E', 'contact_details': 'Contact E', 'address': 'Address E', 'vendor_code': 'VENDOR005'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Delete the vendor
        response = self.client.delete(f'/api/vendors/{vendor_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)



class PurchaseOrderAPITestCase(TestCase):
    '''
        These test cases cover:

        Creating a purchase order (test_purchase_order_list_create_api).
        Retrieving a specific purchase order (test_purchase_order_detail_api).
        Acknowledging a purchase order (test_acknowledge_purchase_order_api).
        Updating a purchase order (test_purchase_order_update_api).
        Deleting a purchase order (test_purchase_order_delete_api).

    '''
    def setUp(self):
        self.client = APIClient()

    def test_purchase_order_list_create_api(self):
        # Create a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor A', 'contact_details': 'Contact A', 'address': 'Address A', 'vendor_code': 'VENDOR001'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Test creating a purchase order
        response = self.client.post('/api/purchase_orders/', {'vendor': vendor_id, 'po_number': 'PO001', 'order_date': '2023-01-01', 'delivery_date': '2023-01-10', 'items': [], 'quantity': 10, 'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)

        # Test listing purchase orders
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_purchase_order_detail_api(self):
        # Create a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor B', 'contact_details': 'Contact B', 'address': 'Address B', 'vendor_code': 'VENDOR002'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Create a purchase order
        response = self.client.post('/api/purchase_orders/', {'vendor': vendor_id, 'po_number': 'PO002', 'order_date': '2023-01-02', 'delivery_date': '2023-01-11', 'items': [], 'quantity': 20, 'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        po_id = response.data['id']

        # Test retrieving a specific purchase order
        response = self.client.get(f'/api/purchase_orders/{po_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'PO002')

    def test_acknowledge_purchase_order_api(self):
        # Create a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor C', 'contact_details': 'Contact C', 'address': 'Address C', 'vendor_code': 'VENDOR003'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Create a purchase order
        response = self.client.post('/api/purchase_orders/', {'vendor': vendor_id, 'po_number': 'PO003', 'order_date': '2023-01-03', 'delivery_date': '2023-01-13', 'items': [], 'quantity': 30, 'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        po_id = response.data['id']

        # Acknowledge the purchase order
        response = self.client.post(f'/api/purchase_orders/{po_id}/acknowledge/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['acknowledgment_date'])

        # Ensure acknowledgment date is updated in the database
        po = PurchaseOrder.objects.get(pk=po_id)
        self.assertIsNotNone(po.acknowledgment_date)

    def test_purchase_order_update_api(self):
        # Create a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor D', 'contact_details': 'Contact D', 'address': 'Address D', 'vendor_code': 'VENDOR004'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Create a purchase order
        response = self.client.post('/api/purchase_orders/', {'vendor': vendor_id, 'po_number': 'PO004', 'order_date': '2023-01-04', 'delivery_date': '2023-01-14', 'items': [], 'quantity': 40, 'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        po_id = response.data['id']

        # Update the purchase order
        updated_data = {'po_number': 'Updated PO004', 'order_date': '2023-01-05', 'delivery_date': '2023-01-15', 'quantity': 50, 'status': 'completed'}
        response = self.client.put(f'/api/purchase_orders/{po_id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'Updated PO004')

    def test_purchase_order_delete_api(self):
        # Create a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor E', 'contact_details': 'Contact E', 'address': 'Address E', 'vendor_code': 'VENDOR005'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Create a purchase order
        response = self.client.post('/api/purchase_orders/', {'vendor': vendor_id, 'po_number': 'PO005', 'order_date': '2023-01-05', 'delivery_date': '2023-01-16', 'items': [], 'quantity': 60, 'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        po_id = response.data['id']

        # Delete the purchase order
        response = self.client.delete(f'/api/purchase_orders/{po_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)
