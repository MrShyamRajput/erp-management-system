# finance/forms.py

from django import forms
from .models import Invoice


class InvoiceForm(forms.ModelForm):

    class Meta:

        model = Invoice

        fields = [

            'client_name',
            'invoice_number',
            'amount',
            'due_date',
            'status'

        ]

        widgets = {

            'client_name': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border-gray-300'
            }),

            'invoice_number': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border-gray-300'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'w-full rounded-xl border-gray-300'
            }),

            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full rounded-xl border-gray-300'
            }),

            'status': forms.Select(attrs={
                'class': 'w-full rounded-xl border-gray-300'
            }),

        }