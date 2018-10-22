from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets, filters

from .models import *

__author__ = "Johannes Pfrang"


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    type = ItemTypeSerializer()

    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    type = ItemTypeSerializer()
    contact = ContactSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = Item
        # every field except the lender (not necessary)
        exclude = ('user',)


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name', 'type__name', 'description', 'categories__name')
    filter_fields = {
        'name': ['exact', 'contains'],
        'type__name': ['exact', 'contains'],
        'description': ['contains'],
        # TODO: support an OR connected manytomany field filter
        'categories__name': ['exact', 'contains'],
    }
