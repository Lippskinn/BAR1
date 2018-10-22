from django.db import models
from django.contrib.auth.models import User

__author__ = "Andreas Kirsch"


class ItemType(models.Model):
    """
        The model ItemType which is used to distinguish between Knowledge and Objects. Done by Andreas Kirsch
    """

    # The name of the ItemType
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Contact(models.Model):
    """
        The model used for storing Contact details of Users OR/AND Item. Done by Andreas Kirsch
    """

    # The name of the person to contact
    name = models.CharField(max_length=128, verbose_name="Name des Ansprechpartners/in")
    # The mail address
    mail = models.EmailField()
    # The phone number (optional)
    phone = models.CharField(max_length=32, blank=True, verbose_name="Telefonnummer")
    # The mobile phone number (optional)
    mobile = models.CharField(max_length=32, blank=True, verbose_name="Handynummer")
    # The fax address (optional)
    fax = models.CharField(max_length=32, blank=True, verbose_name="Fax Nummer")

    def __str__(self):
        return "[Contact] Name=%s, Mail=%s, Fax=%s, Mobile=%s, Phone=%s" \
               % (self.name, self.mail, self.fax, self.mobile, self.phone)


class Lender(models.Model):
    """
        The extended User model allowing to use the default Django User model, but have custom fields.
        Done by Andreas Kirsch
    """

    # The internal user of Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Name")
    # The contact information of that Lender
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name="Kontaktdaten")
    # The name of the organisation (optional)
    organisation = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return "[Lender] User=%s, Contact=%s, Organisation=%s" % (self.user.username, self.contact, self.organisation)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Lender.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.lender.save()


class Category(models.Model):
    """
        The model Category which makes it possible that each Item can have several Categories. Done by Andreas Kirsch
    """

    # The type of the category, (=type of the Item); needed to avoid that e.g. Objects get Knowledge Categories
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, verbose_name="Typ")
    # The name of the category
    name = models.CharField(max_length=64)

    def __str__(self):
        return "%s: %s" % (self.type, self.name)


class Item(models.Model):
    """
        The model Item for a (Object|Knowledge)-Item that is offered in the resource pool. Done by Andreas Kirsch
    """

    # The name of the Item
    name = models.CharField(max_length=128)
    # The type of the Item
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, verbose_name="Typ")
    # The description of the Item
    description = models.TextField(verbose_name="Beschreibung")
    # The contact details of the Item
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    # The user that created the Item
    user = models.ForeignKey(Lender, on_delete=models.CASCADE)
    # The list of Categories for this Item
    categories = models.ManyToManyField(Category, verbose_name="Kategorien")
    # Whether this Item is a gift or a loan
    isGift = models.BooleanField(verbose_name="Als Geschenk anbieten?")
    # Image of the Item (optional)
    image = models.ImageField(upload_to="imgs/items/", blank=True, verbose_name="Bild")
    # The location of the Item as GPS latitude
    latitude = models.FloatField()
    # The location of the Item as GPS longitude
    longitude = models.FloatField()
    # The location of the Item as address that was typed in by the user
    address = models.CharField(max_length=256)
    # The location of the Item as post code that was typed in by the user
    plz = models.IntegerField()

    def __str__(self):
        return self.name
