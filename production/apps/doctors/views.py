from django.shortcuts import render, get_object_or_404
from .models import Doctor, Department

def doctor_list(request):
    doctors = Doctor.objects.all()
    # Filter logic
    dept_slug = request.GET.get('speciality')
    if dept_slug:
        doctors = doctors.filter(department__slug=dept_slug)
        
    specialities = Department.objects.all()
    context = {
        'doctors': doctors,
        'specialities': specialities,
        'selected_dept': dept_slug,
    }
    return render(request, 'doctors/doctor_list.html', context)

def doctor_detail(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'doctors/department_list.html', {'departments': departments})

def department_detail(request, slug):
    department = get_object_or_404(Department, slug=slug)
    doctors = department.doctors.all()
    return render(request, 'doctors/department_detail.html', {
        'department': department,
        'doctors': doctors
    })
