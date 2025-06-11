from django import forms
from .models import Item, Domain, Field, Branch, Author

class ItemFilterForm(forms.Form):
    ITEM_TYPES = [('', 'All')] + Item.ITEM_TYPES
    item_type = forms.ChoiceField(
        choices=ITEM_TYPES, required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    title = forms.CharField(max_length=255, required=False)

    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
        empty_label="All Authors",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    domain = forms.ModelChoiceField(
        queryset=Domain.objects.all(),
        required=False,
        empty_label="All Domains",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    field = forms.ModelChoiceField(
        queryset=Field.objects.all(),
        required=False,
        empty_label="All Fields",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        required=False,
        empty_label="All Branches",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    date_created_from = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'date'})
    )

    date_created_to = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'date'})
    )

    tags = forms.CharField(max_length=255, required=False)
