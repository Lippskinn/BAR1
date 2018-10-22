from django.contrib import admin

from .models import Lender, Contact, Item, ItemType, Category

__author__ = "Johannes Pfrang"

admin.site.register(Lender)
admin.site.register(Contact)
admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(Category)
