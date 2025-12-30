from django.contrib import admin
from .models import MedicineCategory, Medicine, Batch, Sale, SaleItem 

@admin.register(MedicineCategory)
class MedicineCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule_type', 'vendor', 'generic_name', 'category', 'reorder_level')
    list_filter = ('schedule_type', 'category', 'dosage_form')
    search_fields = ('name', 'generic_name', 'manufacturer')

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'batch_number', 'expiry_date', 'quantity', 'buy_price', 'sell_price')
    list_filter = ('expiry_date', 'medicine__category')
    search_fields = ('batch_number', 'medicine__name')
    date_hierarchy = 'expiry_date'

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'get_total', 'status', 'doctor')
    
    def get_total(self, obj):
        if obj.invoice:
            return obj.invoice.total_amount
        return 0.00
    get_total.short_description = 'Total Amount'
    list_filter = ('date',)
    date_hierarchy = 'date'
    inlines = [SaleItemInline]
