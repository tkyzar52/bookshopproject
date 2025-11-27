from django.urls import path
from . import views 


app_name = 'bookshop'

urlpatterns = [
path('',views.IndexView.as_view(), name = 'index'),
path ('photo-detail/<int:pk>/',
      views.BookDetailView.as_view(),
      name='book_detail'),
path('cart/', views.cart_detail, name='cart_detail'),
path('cart/add/<int:book_id>/', views.add_to_cart, 
     name='add_to_cart'),
path('cart/remove/<int:item_id>/', views.remove_cart_item,
     name='remove_cart_item'),
path ('contact/', views.ContactView.as_view(),
      name = 'contact')
]



