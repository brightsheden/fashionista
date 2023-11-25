from django.urls import  path
from .views import *

urlpatterns = [
    path('', home, name='home' ),
    path('product/<str:pk>', product, name='product' ),
    path('blogs/', blog_list, name='blog_list'),
    path('add_product/', add_product, name='add_product'),
   
   
    path('blogs/create/', create_blog, name='create_blog'),
    path('blogs/<int:blog_id>/edit/', edit_blog, name='edit_blog'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]


