from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, F, Q
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator

from .models import Order
from .forms import OrderForm


def create_order(request):

    form = OrderForm()

    # =========================
    # DELETE ORDER
    # =========================
    if request.method == 'POST' and 'delete_id' in request.POST:

        order = get_object_or_404(
            Order,
            id=request.POST.get('delete_id')
        )

        order.delete()

        messages.success(request, "Order deleted successfully!")

        return redirect('create_order')

    # =========================
    # UPDATE ORDER
    # =========================
    if request.method == 'POST' and 'edit_id' in request.POST:

        order = get_object_or_404(
            Order,
            id=request.POST.get('edit_id')
        )

        order.full_name = request.POST.get('full_name')
        order.email = request.POST.get('email')
        order.product = request.POST.get('product')
        order.quantity = request.POST.get('quantity')
        order.price = request.POST.get('price')
        order.status = request.POST.get('status')

        order.save()

        messages.success(request, "Order updated successfully!")

        return redirect('create_order')

    # =========================
    # CREATE ORDER
    # =========================
    if request.method == 'POST' and 'edit_id' not in request.POST:

        form = OrderForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Order created successfully!")

            return redirect('create_order')

        else:
            messages.error(request, "Something went wrong!")

    # =========================
    # FETCH ORDERS
    # =========================
    orders = Order.objects.all().order_by('-created_at')

    # =========================
    # SEARCH
    # =========================
    query = request.GET.get('q')
    status = request.GET.get('status')

    if query:

        orders = orders.filter(

            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(product__icontains=query) |
            Q(status__icontains=query)
        )

    if status:
        orders = orders.filter(status=status)

    # =========================
    # DASHBOARD STATS
    # =========================

    total_customers = Order.objects.values(
        'email'
    ).distinct().count()

    active_orders = Order.objects.exclude(
        status='delivered'
    ).count()

    total_revenue = Order.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0

    pending_returns = Order.objects.filter(
        status='pending'
    ).count()

    # =========================
    # MONTHLY SALES
    # =========================

    monthly_sales = (

        Order.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum(F('price') * F('quantity')))
        .order_by('month')
    )

    max_value = max(
        [m['total'] or 0 for m in monthly_sales],
        default=1
    )

    for m in monthly_sales:

        total = m['total'] or 0

        m['percent'] = (
            (total / max_value) * 100
        ) if max_value else 0

    # =========================
    # PAGINATION
    # =========================

    paginator = Paginator(orders, 5)

    page_number = request.GET.get('page')

    orders = paginator.get_page(page_number)

    context = {

        'form': form,
        'orders': orders,

        'monthly_sales': monthly_sales,

        'total_customers': total_customers,
        'active_orders': active_orders,
        'total_revenue': total_revenue,
        'pending_returns': pending_returns,
    }

    return render(
        request,
        'sales.html',
        context
    )