from django.contrib import admin
from .models import Order, Invoice, Courier, Delivery, Asset, Report

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'order_name', 'expected_date', 'actual_date', 'created_at')
    list_filter = ('expected_date', 'actual_date')
    search_fields = ('order_number', 'order_name')
    date_hierarchy = 'expected_date'

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'order', 'issue_date', 'created_at')
    list_filter = ('issue_date',)
    search_fields = ('invoice_number', 'order__order_number')
    raw_id_fields = ('order',)
    date_hierarchy = 'issue_date'

class CourierAdmin(admin.ModelAdmin):
    list_display = ('courier_fullname', 'courier_phoneno', 'courier_license', 'created_at')
    search_fields = ('courier_fullname', 'courier_license', 'courier_phoneno')
    list_filter = ('created_at',)

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'courier', 'delivery_date', 'status', 'created_at')
    list_filter = ('status', 'delivery_date')
    search_fields = ('order__order_number', 'courier__courier_fullname')
    raw_id_fields = ('order', 'courier')
    date_hierarchy = 'delivery_date'

class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'status', 'location', 'created_at')
    list_filter = ('status', 'location')
    search_fields = ('name', 'serial_number', 'description')
    date_hierarchy = 'created_at'

class ReportAdmin(admin.ModelAdmin):
    list_display = ('temp_no', 'asset_name', 'serial_number', 'asset_code', 'depreciation', 'cost', 'status', 'location', 'created_at')
    list_filter = ('status', 'location')
    search_fields = ('temp_no', 'asset_name', 'serial_number', 'asset_code')
    date_hierarchy = 'created_at'

admin.site.register(Order, OrderAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Courier, CourierAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Report, ReportAdmin)