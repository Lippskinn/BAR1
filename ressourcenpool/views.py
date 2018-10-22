from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.views.generic import View, ListView

from .forms import LenderForm, UserForm, ContactForm, SearchForm, ItemForm, LocationForm, OrganisationForm, LoginForm
from django.core.exceptions import ObjectDoesNotExist
from .models import Contact, Item, Lender, User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from geopy.geocoders import Nominatim

# Setup Nomatim geocoder (Johannes Pfrang)
geolocator = Nominatim(user_agent="ressourcenpool-bamberg", country_bias="DE", timeout=10)

"""
    Put all the authors of one file in here, separated by comma and add a doc line above the function YOU implemented
"""
__author__ = ["Andreas Kirsch", "Johannes Pfrang", "Yaryna Korduba"]


def map(request):
    """ Shows the map search. (Implemented by Johannes Pfrang) """
    return render(request, 'ressourcenpool/map.html')


def register(request):
    """ Registers an user with all the required objects. (Implemented by Sina Fricke and Andreas Kirsch) """
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        print(request.POST)

        profile_form = LenderForm(request.POST)
        contact_form = ContactForm(request.POST)
        user_form = UserForm(request.POST)

        # Create a new user
        if contact_form.is_valid() and user_form.is_valid() and profile_form.is_valid():
            print("checkpoint: all valid")
            # set up contact
            contact = contact_form.save(commit=False)
            res = Contact.objects.all().filter(name=contact.name, phone=contact.phone, mail=contact.mail,
                                               mobile=contact.mobile, fax=contact.fax)
            if res.__len__() > 1:
                contact = res.first()  # if the contact is already in db, reuse it
            else:
                contact.save()
            # set up user
            user = user_form.save(commit=False)
            user.set_password(user.password)
            # set up lender
            lender = profile_form.save(commit=False)
            lender.contact = contact
            lender.organisation = request.POST.get('organisation')

            # when everything is successful, write changes to database
            user.save()
            lender.user = user
            lender.save()
            registered = True  # Update our variable to tell the template registration was successful.
            print("checkpoint: all saved")

    else:
        user_form = UserForm()
        profile_form = LenderForm()
        contact_form = ContactForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'contact_form': contact_form,
        'registered': registered
    }

    return render(request, 'ressourcenpool/register.html', context)


def logon(request):
    """ Does login a user. Implemented by Sina Fricke. Error handling added by Andreas Kirsch """
    login_wrong = False
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                login_wrong = True
    else:
        login_form = LoginForm()
    return render(request, 'ressourcenpool/login.html', {'login_form': login_form, 'error': login_wrong})


def logoff(request):
    """ Logs off a user from the system (Done by Johannes Pfrang, Andreas Kirsch) """
    logout(request)
    return HttpResponseRedirect('/')


def details(request, item_id=-1):
    item = get_object_or_404(Item, pk=item_id)
    fields = item._meta.fields
    # values =  [{'field': field.name, 'value': getattr(item, field.name)} for field in fields]
    item.categories.set(item.categories.all())
    context = {
        'item_id': item_id,
        'item': item,
        'fields': fields,
        'media_url': settings.MEDIA_URL
    }
    return render(request, 'ressourcenpool/offer_display.html', context)


def offer(request, item_id=-1):
    """
        This is the view for creating offers. Implemented by Andreas Kirsch and Johannes Pfrang
    """
    current_user = request.user

    if current_user is None or current_user.is_authenticated is False:
        return redirect('/login')
    try:
        lender = current_user.lender
    except ObjectDoesNotExist:
        lender = None
        return HttpResponse(status=500)

    contact_form = ContactForm(instance=lender.contact)

    # create the empty form just in case
    item_form = ItemForm()
    location_form = LocationForm()

    if item_id is not -1:
        # load in the values from the item id
        try:
            item = Item.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            item = None
            item_id = -1

        if item is not None:
            if item.user.id is not lender.id:
                return HttpResponse(status=403)

            item_form = ItemForm(instance=item)

            location_form = LocationForm(initial={'plz': item.plz, 'address': item.address})
            contact_form = ContactForm(instance=item.contact)

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        item_form = ItemForm(request.POST, request.FILES)
        location_form = LocationForm(request.POST)
        contact = None
        contact_valid = False
        # does the form have a changed contact field ?
        if request.POST.get("editedContact") is not None:
            if contact_form.is_valid():
                contact = contact_form.save(commit=False)
                contact_valid = True
                res = Contact.objects.all().filter(name=contact.name, phone=contact.phone, mail=contact.mail,
                                                   mobile=contact.mobile, fax=contact.fax)
                if res.__len__() > 1:
                    contact = res.first()  # if the contact is already in db, reuse it
                else:
                    contact.save()
        else:  # contact was not changed in form
            contact_valid = True
            contact = lender.contact

        if contact_valid and item_form.is_valid() and location_form.is_valid():

            # when an item was edited and is valid, delete the old item
            if request.POST.get("itemId") is not None:
                item = get_object_or_404(Item, id=request.POST.get("itemId"))
                if item.user.id is not lender.id:
                    return HttpResponse(status=403)
                else:
                    item.delete()

            # TODO: make geocoders safe / return error on geocoder error
            location = geolocator.geocode(
                str(location_form.cleaned_data['plz']) + " " + location_form.cleaned_data['address'])

            # By default use this latitude
            latitude = 49.8988
            longitude = 10.9028

            if location.latitude is not None and location.longitude is not None:
                latitude = location.latitude
                longitude = location.longitude

            item = item_form.save(commit=False)

            item.contact = contact
            item.user = lender
            item.latitude = latitude
            item.longitude = longitude
            item.plz = location_form.cleaned_data['plz']
            item.address = location_form.cleaned_data["address"]

            item.save()

            # in case there were any categories before, clear them !
            item.categories.clear()

            for category in item_form.cleaned_data['categories'].all():
                item.categories.add(category)

            return redirect("/offer/list/")

    context = {
        'item_form': item_form,
        'contact_form': contact_form,
        'location_form': location_form,
        'itemId': item_id
    }

    return render(request, 'ressourcenpool/offer.html', context)


def offers(request):
    """
        This is the view for listing all the offer of ONE Lender to give an overview. Implemented by Andreas Kirsch
    """
    current_user = request.user

    if current_user is None or current_user.is_authenticated is False:
        return redirect('/home')

    try:
        lender = current_user.lender
    except ObjectDoesNotExist:
        return HttpResponse(status=500)

    items = Item.objects.all().filter(user=lender)
    return render(request, 'ressourcenpool/offers.html', {"items": items})


def delete(request, item_id):
    """
        This is the view for deleting an actual Item. Implemented by Andreas Kirsch
    """
    current_user = request.user

    if current_user is None or current_user.is_authenticated is False:
        return redirect('/home')

    try:
        lender = current_user.lender
    except ObjectDoesNotExist:
        lender = None
        return HttpResponse(status=500)

    item = Item.objects.all().get(pk=item_id)
    if item is not None and item.user.id is lender.id:
        item.delete()

    return redirect("/offer/list/")


def account(request):
    """
        This view is used to change user account details by an user. Implemented by Andreas Kirsch
    """
    current_user = request.user

    if current_user is None or current_user.is_authenticated is False:
        return redirect('/login')

    try:
        lender = current_user.lender
    except ObjectDoesNotExist:
        return HttpResponse(status=500)

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        organisation_form = OrganisationForm(request.POST)
        password_form = PasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)

        if organisation_form.is_valid():
            lender.organisation = organisation_form.cleaned_data["organisation"]

        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            res = Contact.objects.all().filter(name=contact.name, phone=contact.phone, mail=contact.mail,
                                               mobile=contact.mobile, fax=contact.fax)
            if res.__len__() > 1:
                contact = res.first()  # if the contact is already in db, reuse it
            else:
                contact.save()

            lender.contact = contact

        lender.save()

    contact_form = ContactForm(instance=lender.contact)
    password_form = PasswordChangeForm(current_user)
    organisation_form = OrganisationForm(initial={"organisation": lender.organisation})

    return render(request, 'ressourcenpool/account.html', {"contact_form": contact_form,
                                                           "password_form": password_form,
                                                           "organisation_form": organisation_form})


def unregister(request):
    """
        Allows to delete a lender / user. Created by Andreas Kirsch
    """

    current_user = request.user
    if current_user is None or current_user.is_authenticated is False:
        return redirect('/login')

    try:
        lender = current_user.lender
    except ObjectDoesNotExist:
        return HttpResponse(status=500)

    lender.delete()
    current_user.delete()

    return redirect('/logout')

# Views for home and info pages added by Yaryna Korduba
def about(request):
    return render(request, 'ressourcenpool/about.html')

def about_project(request):
    return render(request, 'ressourcenpool/about_project.html')

def home(request):
    return render(request, 'ressourcenpool/home.html')


def search(request):

    """
        Allows to search for name/description, type and category. Implemented by Yaryna Korduba
    """

    search_form = SearchForm(request.GET)

    query = request.GET.get('name')
    query1 = request.GET.getlist('type')
    query2 = request.GET.getlist('category')

    items = Item.objects.all().order_by('id')

    if query2:
        items = items.filter(Q(type_id__in=query2))
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if query1:
        items = items.filter(Q(type_id__in=query1))

    page = request.GET.get('page')
    paginator = Paginator(items, 4)
    items = paginator.get_page(page)
    page_range = paginator.page_range
    page_count = paginator.num_pages

    context = {
        'search_form': search_form,
        'items': items,
        'page_range': page_range,
        'page_count': page_count,
        'media_url':  settings.MEDIA_URL
    }
    return render(request, 'ressourcenpool/search.html', context)


# error pages implemented by Julian Kuechler
def error(request):
    return render(request, 'ressourcenpool/templates/404.html')


def error(request):
    return render(request, 'ressourcenpool/templates/500.html')
