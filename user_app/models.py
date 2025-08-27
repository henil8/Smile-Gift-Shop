from django.db import models
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, Group, PermissionsMixin)
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from rest_framework.authtoken.models import Token

# Create your models here.
class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        values = [email]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError("The {} value must be set".format(field_name))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.create(user=user)
        
        if extra_fields['is_superuser']:
            adminGroup, _ = Group.objects.get_or_create(name='Admin')
            adminGroup.user_set.add(user)
            
        return user
    

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
    

class RoleModel(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name'], name='idx_role_name'),
        ]

class CountryModel(models.Model):
    country_name = models.CharField(
        verbose_name='name', max_length=255, unique=True)
    country_code = models.CharField(verbose_name='country code', max_length=3)
    currency = models.CharField(max_length=3)
    calling_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.country_name

class CountryGroupModel(models.Model):
    group_name = models.CharField(max_length=255, verbose_name="group name")
    countries = models.ManyToManyField(CountryModel)

    class Meta:
        verbose_name = 'country group'
        verbose_name_plural = 'country groups'


class StatesModel(models.Model):
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CitiesModel(models.Model):
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)
    state = models.ForeignKey(StatesModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AddressModel(models.Model):
    address_types = (('Office', 'Office'),
                     ('Home', 'Home'), ('Other', 'Other'))
    full_name = models.CharField(max_length=255, blank=True, null=True)
    address_tags = models.CharField(
        choices=address_types, max_length=255, blank=True, null=True)
    mobile = PhoneNumberField(blank=True, null=True)
    another_mobile = PhoneNumberField(blank=True, null=True)
    address_line_1 = models.TextField(blank=True, null=True)
    address_line_2 = models.TextField(blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(CitiesModel, on_delete=models.DO_NOTHING, blank=True, null=True)
    state = models.ForeignKey(StatesModel, on_delete=models.DO_NOTHING, blank=True, null=True)
    postal_code = models.CharField(max_length=10, verbose_name='postal code', blank=True, null=True)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    def __str__(self):
        return f"{self.address_line_1 if self.address_line_1 else ''}, {self.address_line_2 if self.address_line_2 else ''}, {self.landmark if self.landmark else ''}, {self.city.name if self.city else ''}, {self.state.name if self.state else ''}, {self.country.country_name if self.country else ''} - {self.postal_code if self.postal_code else ''}"


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.ForeignKey(RoleModel,on_delete=models.CASCADE,null=True,blank=True)
    mobile_no = PhoneNumberField(null=True,blank=True)
    address = models.ManyToManyField(AddressModel, blank=True)
    approved_status = models.CharField(max_length=100,null=True,blank=True)
    

    
    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def usergroups(self):
        return "".join([l.name for l in self.groups.all()])

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'