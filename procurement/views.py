# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum

from .models import Supplier, PurchaseOrder
from .forms import PurchaseOrderForm


def procurement_dashboard(request):

    # CREATE PURCHASE ORDER
    if request.method == 'POST':

        form = PurchaseOrderForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Purchase Order Created Successfully!"
            )

            return redirect('procurement_dashboard')

        else:

            messages.error(
                request,
                "Form submission failed. Check all fields."
            )

    else:

        form = PurchaseOrderForm()

    # SEARCH
    query = request.GET.get('q')

    orders = PurchaseOrder.objects.select_related(
        'supplier'
    ).all().order_by('-created_at')

    if query:

        orders = orders.filter(
            supplier__name__icontains=query
        )

    # STATS
    total_spend = PurchaseOrder.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_suppliers = Supplier.objects.count()

    pending_orders = PurchaseOrder.objects.exclude(
        status='delivered'
    ).count()

    suppliers = Supplier.objects.all().order_by('-score')[:5]

    context = {

        'form': form,

        'orders': orders,

        'suppliers': suppliers,

        'total_spend': total_spend,

        'total_suppliers': total_suppliers,

        'pending_orders': pending_orders,
    }

    return render(
        request,
        'procurement.html',
        context
    )