from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here. 

class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password, **extra_fields):
        user = self.model(name=name, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save()
        return user

    def create_superuser(self, name, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have staff priviledges')
        return self.create_user(name, email, password, **extra_fields)



class User(AbstractBaseUser):
    first_name =None
    last_name =None
    name = models.CharField( max_length=100)
    email = models.EmailField( unique=True)
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    address = models.CharField(max_length=100,null=True, blank=True,)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()
        
    def __str__(self):
        return self.name

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True



class Category(models.Model):
    category = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.category



class Product(models.Model):
    category = models.ForeignKey(Category, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,default="undefined")
    image = models.ImageField(upload_to='ecommerce/images', default='')
    price = models.IntegerField(default=-1)
    description = models.CharField(max_length=255,default="undefined")
    discount = models.CharField(max_length=255,default="0%")
    final_rate = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.final_rate =self.price -(self.price*(int(self.discount[:-1])/100))
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name 
    

    
class Cart(models.Model):
    customer = models.CharField(max_length=255,default="")
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=1)

    def __str__(self):
        return (str(self.customer) + "-" + str(self.product))