from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Ward, Bed, Admission
from doctors.models import Doctor
from apps.core.validators import validate_phone_number
from django.core.exceptions import ValidationError

@login_required
def admission_dashboard(request):
    wards = Ward.objects.prefetch_related('beds')
    active_admissions = Admission.objects.filter(status='admitted').order_by('-admission_date')
    
    # Calculate stats per ward
    ward_stats = []
    for ward in wards:
        total = ward.beds.count()
        occupied = ward.beds.filter(status='occupied').count()
        available = total - occupied
        ward_stats.append({
            'ward': ward,
            'type_display': ward.get_ward_type_display(),
            'total': total,
            'occupied': occupied,
            'available': available,
            'percent_occupied': (occupied/total)*100 if total > 0 else 0
        })

    context = {
        'ward_stats': ward_stats,
        'active_admissions': active_admissions
    }
    return render(request, 'admissions/dashboard.html', context)

@login_required
def admit_patient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        doctor_id = request.POST.get('doctor')
        bed_id = request.POST.get('bed')
        
        try:
            bed = Bed.objects.get(id=bed_id)
            if bed.status != 'available':
                messages.error(request, "Selected bed is no longer available.")
                return redirect('admissions:admit_patient')
            
            try:
                validate_phone_number(phone)
                
                Admission.objects.create(
                    patient_name=name,
                    patient_phone=phone,
                    patient_age=age,
                    gender=gender,
                    doctor_id=doctor_id,
                    ward=bed.ward,
                    bed=bed,
                    status='admitted'
                )
                messages.success(request, f"Patient {name} admitted successfully to {bed}.")
                return redirect('admissions:dashboard')
                
            except ValidationError as e:
                 # Re-fetch context for rendering
                 doctors = Doctor.objects.all()
                 available_beds = Bed.objects.filter(status='available').select_related('ward').order_by('ward__name', 'bed_number')
                 context = {
                     'doctors': doctors,
                     'available_beds': available_beds,
                     'phone_error': e.message
                 }
                 return render(request, 'admissions/admit_form.html', context)
            
        except Exception as e:
            messages.error(request, f"Error admitting patient: {e}")
    
    # Context for GET
    doctors = Doctor.objects.all()
    # Group available beds by Ward
    available_beds = Bed.objects.filter(status='available').select_related('ward').order_by('ward__name', 'bed_number')
    
    context = {
        'doctors': doctors,
        'available_beds': available_beds
    }
    return render(request, 'admissions/admit_form.html', context)

@login_required
def discharge_patient(request, admission_id):
    admission = get_object_or_404(Admission, id=admission_id)
    if admission.status == 'discharged':
        messages.warning(request, "Patient is already discharged.")
        return redirect('admissions:dashboard')
    
    # Financial Clearance Check
    # We need to import Invoice here inside the function to avoid circular imports 
    # if billing.models imports admissions.models (which it does).
    from billing.models import Invoice
    
    pending_invoices = Invoice.objects.filter(admission=admission, status='pending')
    total_due = sum(inv.total_amount for inv in pending_invoices)
        
    if request.method == 'POST':
        if total_due > 0:
            messages.error(request, f"Cannot discharge patient {admission.patient_name}. Outstanding dues: ₹{total_due}. Please settle invoices first.")
            return redirect('admissions:discharge_patient', admission_id=admission.id)

        notes = request.POST.get('discharge_notes')
        admission.discharge_notes = notes
        admission.status = 'discharged'
        admission.save()
        
        messages.success(request, f"Patient {admission.patient_name} discharged successfully.")
        return redirect('admissions:dashboard')

    context = {
        'admission': admission,
        'pending_invoices': pending_invoices,
        'total_due': total_due,
        'has_dues': total_due > 0
    }
    return render(request, 'admissions/discharge_confirm.html', context)
