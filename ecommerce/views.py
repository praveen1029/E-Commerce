from .models import User, Category, Product, Cart
from .serializers import CategorySerializer, ListProductSerializer, ListAllProductSerializer, DiscountProductSerializer
from .serializers import UserSerializer,ProductSerializer, ContactSerializer, UserRegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

# Create your views here.


# Register API
class RegisterAPI(APIView):
    permission_classes = [AllowAny, ]
    def post(self,request,format=None):
        serializer=UserRegisterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['name']=account.name
            data['email']=account.email
            data['phone']=account.phone
            data['address']=account.address
            return Response("Registeration Successfull")
        else:
            data=serializer.errors
            return Response(data)


# List Category
class ListCategoryAPI(generics.ListAPIView):
    queryset= Category.objects.all()
    serializer_class = CategorySerializer


# List Products
class ListProductAPI(APIView):
    def get(self, request, format=None, **kwargs):
        category = Category.objects.filter(category=kwargs['category'])
        serializer = ListProductSerializer(category, many=True)
        return Response(serializer.data)


# List all Pproducts
class ListAllProductAPI(generics.ListAPIView):
    queryset= Product.objects.all()
    serializer_class = ListAllProductSerializer


# Get product details
class RetreiveProductAPI(generics.RetrieveAPIView):
    queryset= Product.objects.all()
    serializer_class = DiscountProductSerializer


# List product details with discount
class DiscountProductAPI(generics.ListAPIView):
    queryset = Product.objects.exclude(discount="0%")
    serializer_class = DiscountProductSerializer  


# Get user contact information
class ContactAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        return User.objects.filter(name=self.request.user.name)
    serializer_class=ContactSerializer


# Adding product to cart
class AddToCartAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):

        product = kwargs['pk']
        count = request.data['count']

        try:
            customer_data = Cart.objects.get(customer=self.request.user.name, product=product)
        except Cart.DoesNotExist:
            customer_data = None

        try:
            Product.objects.get(id=product)
        except Product.DoesNotExist:
                return Response("Invalid Product ID")

        if customer_data is None:
            for item in Product.objects.filter(id=product):
                price = item.final_rate*count
                Cart.objects.create(customer=self.request.user.name, product=item, price=price, count=count)
                # cart_data = Cart.objects.filter(customer=self.request.user.name)
                # serializer = CartSerializer(cart_data, many=True)
                # return Response(serializer.data)
                return Response("Product Successfully added to cart!")
            try:
                customer_data = Cart.objects.get(customer=self.request.user.name, product=product)
            except Cart.DoesNotExist:
                customer_data = None
            
        else:
            return Response("Product already in Cart!")


# Checkout      
class CheckoutAPI(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, *args, **kwargs):
            
        cart_data = Cart.objects.filter(customer=self.request.user.name)

        if not cart_data:
            return Response("Your Cart is Empty")
        
        total_price = 0
        for item in cart_data:
            total_price += item.price

        subject='Receipt'
        html_content=get_template('receipt.html').render({'cart_data':cart_data,'total_price':total_price})
        from_email=settings.EMAIL_HOST_USER

        msg = EmailMessage(subject, html_content, from_email, [self.request.user.email])
        msg.content_subtype = "html" 
        msg.send()
        Cart.objects.filter(customer=self.request.user.name).delete()
        return Response("Purchase Successfull, Check mail for Receipt")

        
# Add contact information of admin user   
class AdminContactAPI(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    def put(self, request, *args, **kwargs):
        phone = request.data['phone']
        address = request.data['address']
        obj = get_object_or_404(User,id=self.request.user.id)
        obj.phone = phone
        obj.address = address
        obj.save()
        serializer = UserSerializer(obj)
        return Response(serializer.data)


# Create new category
class CategoryCreateAPI(generics.CreateAPIView):
    permission_classes=[IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Create new product
class ProductCreateAPI(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset= Product.objects.all()
    serializer_class = ProductSerializer


# Update products
class ProductUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset= Product.objects.all()
    serializer_class = ProductSerializer


# Delete products
class ProductDeleteAPI(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset= Product.objects.all()
    serializer_class = ProductSerializer


# logout
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)