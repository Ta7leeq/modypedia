from django import forms
from .models import Item

class ItemFilterForm(forms.Form):
    ITEM_TYPES = [('', 'All')] + Item.ITEM_TYPES
    item_type = forms.ChoiceField(choices=ITEM_TYPES, required=False)
    title = forms.CharField(max_length=255, required=False)
    author = forms.CharField(max_length=255, required=False)
    date_created_from = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    date_created_to = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    tags = forms.CharField(max_length=255, required=False)
