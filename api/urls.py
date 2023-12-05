from django.urls import path
from .views import (
    VendorListCreateAPIView,
    VendorDetailAPIView,
    PurchaseOrderListCreateAPIView,
    PurchaseOrderDetailAPIView,
    VendorPerformanceAPIView,
    AcknowledgePurchaseOrderAPIView,
)

urlpatterns = [
    # Vendor URLs
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('vendors/<int:vendor_id>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),

    # Purchase Order URLs
    path('purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderDetailAPIView.as_view(), name='purchase-order-detail'),

    # Acknowledge Purchase Order URL
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='acknowledge-purchase-order'),
]
