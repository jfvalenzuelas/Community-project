from django import forms
from .models import Product
from django.utils.translation import gettext as _

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title',
            'description',
            'price',
            'category'
        )
        
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'price': _('Price'),
            'category': _('Category')
        }

        help_texts = {
            'title': _('Enter a title for the product'),
            'description': _('Enter a description for the product'),
            'price': _('Enter a price for the product'),
            'category': _('Select a category for the product'),
        }

        error_messages = {
            'title': {
                'required': _('Please, enter a title for the product') 
            },
            'description': {
                'required': _('Please, enter a description for the product')
            },
            'price': {
                'required': _('Please, enter a price for the product')
            },
            'category': {
                'required': _('Please, select a category for the product')
            }
        }
