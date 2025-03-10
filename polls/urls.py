from django.urls import path
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('', views.home_view, name='index'),
    path('shop/', views.shop_view, name='shop'),
    path('about/', views.about_view, name='about'),
    path('blog/', views.blog_view, name='blog'),
    path('cart/', views.show_cart, name='cart'),     
    path('checkout/', views.checkout_view, name='checkout'),  # Fixed casing
    path('contact/', views.contact_view, name='contact'), 
    path('services/', views.services_view, name='services'),
    path('thankyou/', views.thankyou_view, name='thankyou'),
    path('signup/', views.signup, name='signup'),  # Fixed duplicate name
    path('login/', views.login_view, name='login_page'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),  # Fixed naming convention
    path('logout/', views.logout, name='logout'),  
    path('update-cart/', views.update_cart, name='update_cart'),
    path('delete-cart/', views.delete_cart, name='delete_cart'),   
    path('orders/', views.order, name='orders'),   
    path('search/', views.search, name='search'),   
    # Payment-related URL  
    path('payment-cart/', views.payment_cart, name='payment'),   
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    