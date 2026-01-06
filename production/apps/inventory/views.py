from django.shortcuts import render, redirect, get_object_or_404
from core.decorators import group_required
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse

from .models import Equipment, MaintenanceContract, Vendor, Consumable, MaintenanceLog
from .forms import EquipmentForm, AMCForm, VendorForm, ConsumableForm, MaintenanceLogForm
from pharmacy.models import Batch  # Import Batch model

@login_required
@group_required('Inventory Managers')
def amc_expiry_dashboard(request):
    today = timezone.now().date()
    next_30_days = today + timedelta(days=30)
    
    # AMCs expiring in the next 30 days
    expiring_amcs = MaintenanceContract.objects.filter(
        contract_end__gte=today,
        contract_end__lte=next_30_days
    ).order_by('contract_end')
    
    # Overdue AMCs (Expired)
    expired_amcs = MaintenanceContract.objects.filter(
        contract_end__lt=today
    ).order_by('-contract_end')

    # Low Stock Consumables
    low_stock_items = [c for c in Consumable.objects.all() if c.is_low_stock()]
    
    # Expiring Medicines (from Pharmacy)
    expiring_medicines = Batch.objects.filter(
        expiry_date__gte=today,
        expiry_date__lte=next_30_days,
        quantity__gt=0
    ).select_related('medicine').order_by('expiry_date')
    
    total_equipment = Equipment.objects.count()
    under_repair = Equipment.objects.filter(status='repair').count()
    total_vendors = Vendor.objects.count()
    total_consumables = Consumable.objects.count()
    
    # Counts for badges
    amc_alert_count = len(expiring_amcs) + len(expired_amcs)
    low_stock_count = len(low_stock_items)
    med_expiry_count = expiring_medicines.count()

    context = {
        'expiring_amcs': expiring_amcs,
        'expired_amcs': expired_amcs,
        'total_equipment': total_equipment,
        'under_repair': under_repair,
        'low_stock_items': low_stock_items,
        'expiring_medicines': expiring_medicines,
        'amc_alert_count': amc_alert_count,
        'low_stock_count': low_stock_count,
        'med_expiry_count': med_expiry_count,
        'total_vendors': total_vendors,
        'total_consumables': total_consumables,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
@group_required('Inventory Managers')
def inventory_list(request):
    equipment_list = Equipment.objects.all().select_related('category', 'vendor').order_by('name')
    
    # Optional: Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        equipment_list = equipment_list.filter(status=status_filter)
    
    # Calculate simple depreciation for display (straight line, assuming 10% residual)
    for unit in equipment_list:
        if unit.cost and unit.purchase_date:
            age_days = (timezone.now().date() - unit.purchase_date).days
            age_years = age_days / 365.25
            if unit.useful_life > 0:
                depreciation_per_year = (float(unit.cost) * 0.9) / unit.useful_life
                current_value = float(unit.cost) - (depreciation_per_year * age_years)
                unit.current_value = max(current_value, float(unit.cost) * 0.1) # Min is residual
            else:
                unit.current_value = unit.cost
        else:
            unit.current_value = 0

    return render(request, 'inventory/list.html', {
        'equipment_list': equipment_list,
        'status_filter': status_filter
    })

# --- Equipment CRUD ---
@login_required
@group_required('Inventory Managers')
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = EquipmentForm()
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Add Equipment'})

@login_required
@group_required('Inventory Managers')
def edit_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Edit Equipment'})

# --- Vendor CRUD ---
@login_required
@group_required('Inventory Managers')
def vendor_list(request):
    vendors = Vendor.objects.all().order_by('name')
    return render(request, 'inventory/vendor_list.html', {'vendors': vendors})

@login_required
@group_required('Inventory Managers')
def add_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm()
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Add Vendor'})

@login_required
@group_required('Inventory Managers')
def edit_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Edit Vendor'})

# --- Consumable CRUD ---
@login_required
@group_required('Inventory Managers')
def consumable_list(request):
    consumables = Consumable.objects.all().select_related('vendor').order_by('name')
    return render(request, 'inventory/consumable_list.html', {'consumables': consumables})

@login_required
@group_required('Inventory Managers')
def add_consumable(request):
    if request.method == 'POST':
        form = ConsumableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consumable_list')
    else:
        form = ConsumableForm()
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Add Consumable'})

@login_required
@group_required('Inventory Managers')
def edit_consumable(request, pk):
    item = get_object_or_404(Consumable, pk=pk)
    if request.method == 'POST':
        form = ConsumableForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('consumable_list')
    else:
        form = ConsumableForm(instance=item)
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Edit Consumable'})

# --- AMC CRUD ---
@login_required
@group_required('Inventory Managers')
def amc_list(request):
    amcs = MaintenanceContract.objects.all().select_related('equipment', 'vendor').order_by('contract_end')
    
    # Check for active status
    today = timezone.now().date()
    for amc in amcs:
        amc.is_active = amc.contract_end >= today

    return render(request, 'inventory/amc_list.html', {'amcs': amcs, 'today': today})

@login_required
@group_required('Inventory Managers')
def add_amc(request):
    # Pre-check for dependencies
    equipment_count = Equipment.objects.count()
    vendor_count = Vendor.objects.count()
    
    warnings = []
    if equipment_count == 0:
        warnings.append({
            'msg': "There is no equipment in our inventory.",
            'link': 'add_equipment',
            'link_text': 'Add Equipment Now'
        })
    
    if vendor_count == 0:
        warnings.append({
            'msg': "There is no vendor in our list.",
            'link': 'add_vendor',
            'link_text': 'Add Vendor Now'
        })
        
    if warnings:
        return render(request, 'inventory/form.html', {
            'warnings': warnings, 
            'title': 'Add Maintenance Contract',
            'form': None # Do not show form
        })

    if request.method == 'POST':
        form = AMCForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_dashboard')
    else:
        form = AMCForm()
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Add Maintenance Contract'})

@login_required
@group_required('Inventory Managers')
def edit_amc(request, pk):
    amc = get_object_or_404(MaintenanceContract, pk=pk)
    if request.method == 'POST':
        form = AMCForm(request.POST, instance=amc)
        if form.is_valid():
            form.save()
            return redirect('inventory_dashboard')
    else:
        form = AMCForm(instance=amc)
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Edit Maintenance Contract'})

# --- Maintenance Logs ---
@login_required
@group_required('Inventory Managers')
def maintenance_log_list(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    logs = equipment.maintenance_logs.all().order_by('-date')
    return render(request, 'inventory/log_list.html', {'equipment': equipment, 'logs': logs})

@login_required
@group_required('Inventory Managers')
def add_maintenance_log(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if request.method == 'POST':
        form = MaintenanceLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.equipment = equipment
            log.save()
            return redirect('maintenance_log_list', equipment_id=equipment.id)
    else:
        form = MaintenanceLogForm(initial={'equipment': equipment})
    return render(request, 'inventory/form.html', {'form': form, 'title': f'Add Log for {equipment.name}'})

# --- QR Code ---
@login_required
@group_required('Inventory Managers')
def view_qr(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if not equipment.qr_code:
        # Trigger save to generate QR if missing
        equipment.save()
    
    return render(request, 'inventory/view_qr.html', {'equipment': equipment})
