from django import forms
from django.contrib.auth.models import User
from .models import Lender, Contact, Item, Category, ItemType

__author__ = "Andreas Kirsch"

# Styled by Yaryna Korduba and Julian Küchler



"""Lets user login. Implemented by Sina Fricke"""


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].help_text = None

"""Registers a new User. Implemented by Sina Fricke. """


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email' , 'password', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].help_text=None


class LenderForm(forms.ModelForm):
    class Meta:
        model = Lender
        fields = ('organisation',)


class ContactForm(forms.ModelForm):
    """
        Allows to create a Contact Model using Django Forms (created by Andreas Kirsch)
    """
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['mail'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['mobile'].widget.attrs.update({'class': 'form-control'})
        self.fields['fax'].widget.attrs.update({'class': 'form-control'})


class ItemForm(forms.ModelForm):
    """
        Allows to create a Item Model using Django Forms (created by Andreas Kirsch)
    """
    categories = forms.ModelMultipleChoiceField(\
        label="Categories", required=False, queryset=Category.objects.all(),\
        widget=forms.CheckboxSelectMultiple( \
        attrs={'class': "list-unstyled mb-0 category__list", "id": "Categories",\
        "name": "categories"}))

    class Meta:
        model = Item
        fields = ["name", "type", "isGift", "description", "categories", "image"]

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control col-md-6'})
        self.fields['type'].widget.attrs.update({'class': 'form-control col-md-6'})
        self.fields['description'].widget.attrs.update({'class': 'form-control col-md-6'})


class LocationForm(forms.Form):
    """
        Allows to create a Location object, that will not be resolved into a model, since locations are not stored as object
        (created by Andreas Kirsch and Johannes Pfrang)
    """
    plz = forms.IntegerField(label="Postleitzahl", min_value=10000, max_value=99999)
    address = forms.CharField(min_length=1, label="Adresse (Straße und Hausnummer)")

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['plz'].widget.attrs.update({'class': 'form-control col-md-6'})
        self.fields['address'].widget.attrs.update({'class': 'form-control col-md-6'})


class OrganisationForm(forms.Form):
    """
        Field for the organisation (created by Andreas Kirsch)
    """
    organisation = forms.CharField(label='Organisation', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))


# Search form created by Yaryna Korduba
# allows searching with name/description, categories and types
class SearchForm(forms.Form):

    name = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'q','placeholder':"Suche nach Dingen zum Leihen..."}))
    type = forms.ModelMultipleChoiceField(label="", required=False, queryset=ItemType.objects.all(),  widget=forms.SelectMultiple(attrs={'class': "form-control", "id":"Type", "name": "type"}))
    category = forms.ModelMultipleChoiceField(label="", required=False, queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': "list-unstyled mb-0", "id":"Category", "name": "category"}))

class CategoryForm(forms.Form):
    category = forms.ModelMultipleChoiceField(label="", required=False, queryset=Category.objects.all(), widget=forms.SelectMultiple(attrs={'class': "form-control", "id":"Category", "name": "category"}))