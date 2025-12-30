from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Invoice

@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST' and 'mark_paid' in request.POST:
        invoice.status = 'paid'
        invoice.save()
        # Ideally we would create a Payment record here too, but for now just updating status is sufficient per user request.
        return redirect('billing:invoice_detail', invoice_id=invoice.id)
        
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})

@login_required
def dashboard(request):
    invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'billing/dashboard.html', {'invoices': invoices})
