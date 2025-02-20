from django.db import models

# Create your models here.
# Create your models here.
class Product(models.Model) :
    image = models.ImageField(upload_to='products/') 
    name = models.CharField(max_length=50,blank=True, null=True)
    price = models.IntegerField(default=1,blank=True, null=True)    

    def get_all_products() :
        return Product.objects.all()  

    def __str__(self) :
        return self.name 
    
class Customer(models.Model) :    
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15)
    # mail = models.CharField(max_length=35, blank=True, null=True)

    def register(self) :
        self.save() 


    # Customer.objects.filter(phone=self.phone): # This constructs a query set of Customer objects where the phone field
    #  matches self.phone.
    def isExists(self) :
        if Customer.objects.filter(phone=self.phone) : # it checks if there are any records in the Customer table where
            return True                                #  the phone field matches the phone attribute of the current 
        else :                                         # instance === (self.phone). ==== === Current number Apse at le ke 
            return False                               # check kar se. ======

class gallery_view(models.Model) :
    image = models.ImageField(upload_to='gallery/') 
    name = models.CharField(max_length=50,blank=True, null=True)
    price = models.IntegerField(default=1,blank=True, null=True)    

    def get_all_gallery_view() :
        return gallery_view.objects.all()  
         
    def __str__(self) :
        return self.name      

class Cart(models.Model) :
    phone = models.IntegerField(blank=True, null=True) 
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    image = models.ImageField(blank=True,null=True)
    quantity = models.PositiveIntegerField(default=1)  
    price = models.IntegerField(default=1)


    def get_all_cart() :
        return Cart.objects.all()
    

STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way','On the Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)
    
class OrderDetail(models.Model) :
    user = models.IntegerField(default=True)
    product_name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending',choices=STATUS_CHOICE)         

class Paymentcart(models.Model) :
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)