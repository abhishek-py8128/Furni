from django.contrib import admin
from polls.models import Product, Customer, Cart, gallery_view, OrderDetail, Paymentcart

# Register your models here.
class AdminProduct(admin.ModelAdmin) :
    list_display = ['id','image','name','price']

class AdminCustomer(admin.ModelAdmin) :
    list_display = ['id','name','phone']

class Admingallery_view(admin.ModelAdmin) :
    list_display = ['id','image','name','price']

class AdminCart(admin.ModelAdmin) :
    list_display = ['id','phone','product','image','quantity','price']    

class AdminOrderDetail(admin.ModelAdmin) :
    list_display = ['id', 'user', 'product_name', 'quantity', 'image', 'price', 'status', 'order_date']    

class AdminPaymentcart(admin.ModelAdmin) :
    list_display = ['id', 'amount', 'payment_id', 'paid']    

admin.site.register(Product,AdminProduct)    
admin.site.register(gallery_view,Admingallery_view)
admin.site.register(Cart,AdminCart)
admin.site.register(Customer,AdminCustomer)
admin.site.register(OrderDetail, AdminOrderDetail)
admin.site.register(Paymentcart, AdminPaymentcart)