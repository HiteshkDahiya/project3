from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('index/',views.index,name='index'),
    path('logout/',views.log_out,name='logout'),
    path('profile_data/',views.profile_data,name='profile_data'),
    path('show_cart/',views.show_cart_data,name='show_cart_data'),
    path('delete_cart/<int:id>/', views.delete_cart_data, name='delete_cart_data'),
    path('show_wish/',views.show_wish_data,name='show_wish_data'),
    path('delete_wish/<int:id>/', views.delete_wish_data, name='delete_wish_data'),
    path('add_item/',views.add_item,name='add_item'),
    path('add_images/<int:id>/',views.add_images,name='add_images'),
    path('add_variants/<int:id>/',views.add_variants,name='add_variants'),
    path('delete_item/<int:id>/',views.delete_item,name='delete_item'),
    path('edit_item/<int:id>/',views.edit_item,name='edit_item'),
    path('show_detail/<int:id>/', views.show_detail,name='show_detail'),
    path('wishlist-toggle/', views.toggle_wishlist, name='wishlist_toggle'),
    path('cartlist-toggle/', views.toggle_cartlist, name='cartlist_toggle'),
    path('men_shoes/', views.men_shoes, name='men-shoes'),
    path('check_pin/<int:pin>/', views.check_pincode, name='check_pin'),
    path('women_shoes/', views.women_shoes, name='women-shoes'),
    path('testing/', views.testing, name='testing'),
    path('mailme/', views.send_Email, name='mail'),
    path('verify/', views.verify_payment, name='payment_verify'),
    path('purchase_order/', views.order_history, name='orders'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




