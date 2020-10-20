from django import forms
from .models import MarketCategory
from django.utils.translation import gettext as _

class MarketPostForm(forms.Form):
    title = forms.CharField(label=_('Title'), help_text='Give your Post a Title.', error_messages={'required': 'Please give your Post a Title.'}, required=True, max_length=255)
    name = forms.CharField(label=_('Product'), help_text='Give your Product a Name.', error_messages={'required': 'Please give your Product a Name.'}, required=True, max_length=255)
    description = forms.CharField(widget=forms.Textarea, label=_('Description'), help_text='Write a nice description for your product.', error_messages={'required': 'Please give your Product a Description.'}, required=True)
    price = forms.DecimalField(label=_('Price'), help_text='The right price for your Product.', error_messages={'required': 'Please give your Product a Price.'}, required=True, max_digits=10, decimal_places=2)
    category = forms.ChoiceField(label=_('Category'), help_text='Give a Category for your Product.', error_messages={'required': 'Please select a Category.'}, required=True)
    image = forms.ImageField(label=_('Photo'), help_text='Upload a Picture of your Product.', required=False)

    def __init__(self, *args, submission=None):
        super().__init__(*args)
        self.submission = submission

        # Fill available market categories
        available_market_categories = MarketCategory.objects.exclude(active=False)
    
        categories = list(available_market_categories)
        self.fields['category'].choices = (
            (category.title.lower(),
            category.title)
            for category in categories
        )