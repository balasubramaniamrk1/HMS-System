from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('pos/', views.pos_view, name='pos'),
    path('dashboard/', views.pharmacy_dashboard, name='dashboard'),
    path('stock/', views.stock_list, name='stock_list'),
    path('inventory/', views.stock_list, name='inventory'), # Legacy alias
    path('return/', views.return_medicine, name='return_medicine'),
    path('medicine/add/', views.medicine_create, name='medicine_create'),
    
    # Purchase Management
    path('purchase-orders/', views.purchase_order_list, name='purchase_order_list'),
    path('purchase-orders/<int:pk>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('purchase-orders/new/', views.purchase_order_create, name='purchase_order_create'),
    path('stock/entry/', views.stock_entry_create, name='stock_entry_create'),
    
    # Reports
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('reports/sales/', views.sales_report, name='report_sales'),
    path('reports/expiry/', views.expiry_report, name='report_expiry'),
    path('reports/stock/', views.stock_report, name='report_stock'),
    path('reports/returns/', views.returns_report, name='report_returns'),
]
