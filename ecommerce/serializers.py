from rest_framework import serializers
from .models import User, Category, Product, Cart

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','email','phone','address','password']
        
    def save(self):
        reg=User(
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            address=self.validated_data['address'],
        )
        password=self.validated_data['password']        
        reg.set_password(password)
        reg.save()
        return reg


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=['is_staff','is_active','is_superuser',"password",'last_login']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'


class ProductNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['name']


class ListAllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name']


class DiscountProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        exclude=['category']


class ListProductSerializer(serializers.ModelSerializer):
    product_set = ProductNameSerializer(many=True)
    class Meta:
        model = Category
        fields = ['category','product_set']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['email','phone','address']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['product']