import re

from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve

from . import views

"""
This is a main file, and everyone who needed a new URL to be available simply added it
"""
__author__ = "Everyone"

urlpatterns = [
    path('', views.home),
    # search map
    path('map/', views.map),
    # item details
    path('details/<int:item_id>/', views.details),
    # pages for item administration
    path('offer/', views.offer),  # create offer
    path('offer/<int:item_id>/', views.offer),  # edit offer
    path('offer/list/', views.offers),  # list all offers of a user
    path('offer/delete/<int:item_id>/', views.delete),  # delete an offer
    path('account/', views.account),  # overview over account details
    path('unregister/', views.unregister),  # delete an user / lender
    # registration for people lending stuff
    path('register/', views.register),
    # generic stuff
    path('about/', views.about),
    path('about_project/', views.about_project),
    path('home/', views.home),
    path('login/', views.logon),
    path('logout/', views.logoff),
    path('search/', views.search)
    #path(r'^results/$', views.search, name="search")
    #path('impressum/', views.impressum),
]


""" Below implemented by Johannes Pfrang """


# from django.conf.urls.static w/o debug checks
def force_static(prefix, view=serve, **kwargs):
    return [re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs)]


# Force django to serve statics even if not in DEBUG mode
# Note: This requires running `manage.py collectstatic`!
if not settings.DEBUG:
    urlpatterns += force_static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Always serve media files directly
urlpatterns += force_static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

############
# REST API #
############
from rest_framework import routers
from .api_views import ItemViewSet

router = routers.DefaultRouter()
router.register('items', ItemViewSet)
urlpatterns += [
    path('api/', include(router.urls))
]
