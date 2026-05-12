# forms.py

from django import forms
from .models import Supplier, PurchaseOrder


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = '__all__'


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder

        fields = [
            'supplier',
            'item_name',
            'quantity',
            'estimated_delivery',
            'amount',
            'status'
        ]

        widgets = {

            'supplier': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),

            'item_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter item name'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Quantity'
            }),

            'estimated_delivery': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Amount'
            }),

            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }