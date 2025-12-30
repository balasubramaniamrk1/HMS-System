from django.contrib import admin
from .models import Invoice, InvoiceItem, Payment

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'date', 'total_amount', 'status', 'source')
    list_filter = ('status', 'source', 'date')
    search_fields = ('patient_name',)
    inlines = [InvoiceItemInline, PaymentInline]

admin.site.register(Payment)
