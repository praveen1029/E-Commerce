from django.urls import path
from . import views



urlpatterns = [

    path("register/",views.RegisterAPI.as_view(),name='registeration'),

    path("category/",views.ListCategoryAPI.as_view(),name='category'),
    path("category/<str:category>/",views.ListProductAPI.as_view(),name='product'),
    path("product/",views.ListAllProductAPI.as_view(),name='allproduct'),
    path("product/<int:pk>/",views.RetreiveProductAPI.as_view(),name='singleproduct'),
    path("discount/",views.DiscountProductAPI.as_view(),name='discount'),
    path("my_contact/",views.ContactAPI.as_view(),name='contact'),
    path("addtocart/<int:pk>/",views.AddToCartAPI.as_view(),name='addtocart'),
    path("checkout/",views.CheckoutAPI.as_view(),name='checkout'),

    path("contact/",views.AdminContactAPI.as_view(),name='admincontact'),
    path("create/category/",views.CategoryCreateAPI.as_view(),name='categorycreate'),
    path("create/product/",views.ProductCreateAPI.as_view(),name='productcreate'),
    path("update/product/<int:pk>/",views.ProductUpdateAPI.as_view(),name='productupdate'),
    path("delete/product/<int:pk>/",views.ProductDeleteAPI.as_view(),name='productdelete'),

    path("logout/",views.LogoutAPI.as_view(),name='logout')
]
