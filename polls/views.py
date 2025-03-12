from django.contrib import messages 
from django.db.models import Q 
from django.shortcuts import render, redirect, HttpResponse 
from polls.models import Product, Customer, Cart, gallery_view, OrderDetail, Paymentcart
from django.shortcuts import get_object_or_404 
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

def home_view(request):
    set = gallery_view.get_all_gallery_view() # get all gallery Images products
    # print('Actual Data print',set)
    print('gallery_view Data', set)
    totalItem = 0  
    # print('You are',request.session.get('phone'))
      
    if request.session.has_key('phone') :
        phone = request.session['phone'] 

        totalItem = len(Cart.objects.filter(phone=phone))

        customer = Customer.objects.filter(phone=phone) 
        for c in customer :
            name = c.name 
            
        data = {
            'set' : set,
            'name' : name,
            'totalItem' : totalItem
        }    
        
        return render(request, 'index.html',data)

    else :
        return redirect('login_page')    

def about_view(request) :
    totalItem = 0  

    if request.session.has_key('phone') :
        phone = request.session['phone']        
        
        totalItem = len(Cart.objects.filter(phone=phone))
        customer = Customer.objects.filter(phone=phone) 
    
        for c in customer :
            name = c.name 

        return render(request, 'about.html',{'name':name, 'totalItem':totalItem})

    else :
        return redirect('login_page')
    
def blog_view(request) :
    totalItem = 0  

    if request.session.has_key('phone') :
        phone = request.session['phone']
        
        totalItem = len(Cart.objects.filter(phone=phone))
        customer = Customer.objects.filter(phone=phone)

        for c in customer :
            name = c.name 

        return render(request, 'blog.html',{'name':name, 'totalItem':totalItem})

    else :
        return redirect('login_page')
    
def contact_view(request) :
    totalItem = 0  

    if request.session.has_key('phone') :
        phone = request.session['phone']
        
        totalItem = len(Cart.objects.filter(phone=phone))
        customer = Customer.objects.filter(phone=phone) 

        for c in customer :
            name = c.name 

        return render(request, 'contact.html',{'name':name, 'totalItem':totalItem})
    else :
        return redirect('login_page')
    
def services_view(request) :
    if request.session.has_key('phone') :
        set = gallery_view.get_all_gallery_view()
        # print('Services Data print',set)

        totalItem = 0

        phone = request.session['phone']
        totalItem = len(Cart.objects.filter(phone=phone))
    
        customer = Customer.objects.filter(phone=phone) 
        for c in customer :
            name = c.name 

        data = {
            'set': set,
            'name' : name,
            'totalItem' : totalItem
        }  

        return render(request, 'services.html',data)

    else :
        return redirect('login_page')
    
def shop_view(request):
    if request.session.has_key('phone') :
        products = Product.get_all_products()  # all product get

        totalItem = 0

        phone = request.session['phone']
        totalItem = len(Cart.objects.filter(phone=phone))

        customer = Customer.objects.filter(phone=phone) 
        for c in customer :
            name = c.name 
        
        data = {
            'products': products,
            'name' : name,
            'totalItem' : totalItem
        }
        
        return render(request, 'shop.html', data)

    else :
        return redirect('login_page')
    
# =========================Signup==============================
@csrf_protect
def signup(request) :
    # print(request.method) # check for the method 

    if request.method == 'GET':
        return render(request, 'login_page.html')

    else:
        postData = request.POST
        name = postData.get('name')
        # mail = postData.get('mail')
        phone = postData.get('phone')
        print(name, phone)

        error_message = None

        value = {
            'phone' : phone,
            'name' : name,
            # 'mail' : mail
        }

        customer = Customer(name=name, phone=phone)  # Ensure Customer model is correct

        # ==== Validation set ====
        if not name:
            error_message = 'Name is Required'
        
        elif not phone:
            error_message = 'Mobile number is Required'
        
        elif len(phone) < 10:
            error_message = 'Mobile Number Must be 10 Characters Long or More'

         # ==== phone number unique hovo joyo ye ====
        elif customer.isExists() : #  user Id unique hoy tame phone number hovo joyo ye 
            error_message = 'Mobile Number Already Exists'    

        if error_message:
            data = {
                'error' : error_message,
                'value' : value
            }
            return render(request, 'login_page.html',data)
        
        else:
            messages.success(request, 'Congratulations! Registration Successful')
            customer.register()
            return redirect('signup')
           
    return render(request, 'login_page.html')        

# =========================Login============================== 
@csrf_protect
def login_view(request) :
    if request.method == 'GET' :
        return render(request, 'login_page.html')
    else :
        phone = request.POST.get('phone')
        # mail = request.POST.get('mail')
        error_message = None

        value = {
            # 'mail' : mail, 
            'phone' : phone
        }

        # phone=request.POST['phone'] ====> It means that only ===== those records where the phone field matches the 
        # value ===== provided in request.POST['phone'] will be retrieved.

        # request.POST is a dictionary-like object that contains all the === data sent in the HTTP POST request. === 
        # request.POST['phone'] extracts the ===== value of the phone field from this data =====.
        customer = Customer.objects.filter(phone=request.POST['phone'])
        
        if customer :
            # is used to store a value in the user's session data ===== Information Server par hold karin rake =====
            
            request.session['phone'] = phone  # ====> The line of code stores the value of the phone variable in the 
            return redirect('/')              # session data under the key 'phone'. <=====
        else :
            error_message = 'Mobile Number is Invalid !!'
            data = {
                'error' : error_message, 
                'value' : value
            }

        return render(request, 'login_page.html',data)

# =========================Logout============================== 

def logout(request) :

    if request.session.has_key('phone') :
        del request.session['phone']
        return redirect(f'/login')
    
    else :
        return redirect('login_page')         
    
# =========================Add_to_cart==============================


def add_to_cart(request) :
    # Get user phone from session
    phone = request.session['phone']   # ====> user 

    if not phone :
        # Handle the case where phone is not in session (user is not logged in)
        messages.error(request, "You need to log in to add items to the cart.")
        return redirect('/login')  # Redirect to login page or handle appropriately

    product_id = request.GET.get('prod_id')    
    print('Id is',product_id)

    product_name = Product.objects.get(id=product_id)
    product = Product.objects.filter(id=product_id)

    for p in product : # product ma thi image and price get karva mate product lidhu che 
        image = p.image
        price = p.price 

    # After call Card models

    Cart(phone=phone, product=product_name, image=image, price=price).save()
    # equal thi pehla je name che te Card model ne column field che .

    return redirect(f"/shop")     

# =========================Products-Details============================== 

def products_details(request) :

    if request.session.has_key['phone'] :
        phone = request.session['phone'] 
        
        totalItem = 0
        product = Product.objects.get() # pass pk
        item_already_in_cart = None

        totalItem = len(Cart.objects.filter(phone=phone))

        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(phone=phone)).exists()
        customer = Customer.objects.filter(phone=phone)

        for c in customer :
            name = c.name 

        data = {
            'product' : product,
            'item_already_in_cart' : item_already_in_cart,
            'name' : name,
            'totalItem' : totalItem
        }   
        return render(request, 'product.html',data)    
   
    else :
        return redirect('login_page')
        
# =========================Show-cart-Details============================== 

def show_cart(request):
    totalItem = 0

    if request.session.has_key('phone') :
        phone = request.session['phone'] 
        totalItem = len(Cart.objects.filter(phone=phone))

        # Fetch all cart items
        cart = Cart.objects.filter(phone=phone)  # Means's ==== cart_items = Cart.get_all_cart() ====
         
        grand_total = 0 

        # Calculate total for each item and the grand total
        for item in cart:
            item.total = item.price * item.quantity
            grand_total += item.total  
      
        customer = Customer.objects.filter(phone=phone)
        for c in customer :
            name = c.name  
             
        data = {
            'name' : name,
            'totalItem' : totalItem,
            'cart' : cart,
            'grand_total': grand_total
        }
           
        if cart :
                return render(request, 'cart.html',data)
            
        else :
            customer = Customer.objects.filter(phone=phone)
            for c in customer :
                name = c.name   
            return render(request, 'cart.html', {'name':name})
    else :
        return redirect('login_page')    
                               
# =========================Cart-Quantity-Update============================== 

def update_cart(request):   
    item_id = request.GET.get('update_get')
    action = request.GET.get('action')  # assuming 'action' determines plus or minus
    print('Action',action)

    if item_id:
        # cart_item = get_object_or_404(Cart, id=item_id)
        cart_item = Cart.objects.filter(id=item_id).first()
        if action == 'plus':
            cart_item.quantity += 1
        elif action == 'minus':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
        cart_item.save()
    return redirect(f'/cart')

# =========================Cart-products Delete============================== 

def delete_cart(request) :
    if request.method == 'POST' :
        delId = request.POST.get('del_id') 
        if delId:
            print('deleted id is', delId)
            cart_item = Cart.objects.filter(id=delId).first()  # Fetch the cart item to be deleted
            if cart_item:
                cart_item.delete()
                return redirect(f'/cart')
        return redirect(f'/cart')  
        
    else :
        return HttpResponse('page does not found')   
     
# =============================Orders Section=================================      
            
def checkout_view(request) :
    # Billings Details
    if request.session.has_key('phone') :
        phone = request.session['phone']
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        cart_product = Cart.objects.filter(phone=phone) 

        grand_total = 0 
        for item in cart_product:
            item.total = item.price * item.quantity
            grand_total += item.total  
            
        context = {
            'grand_total' : grand_total,
        }    
        
        for c in cart_product :
            quantity = c.quantity
            price = c.price
            product_name = c.product
            image = c.image

            OrderDetail(user=phone, product_name=product_name, image=image, price=price, quantity=quantity).save()
            # cart_product.delete()
       
        return render(request, 'checkout.html', context)
    
    else :
        return redirect('login_page')
    
# =============================Orders-Show=================================      

def order(request) :
    totalItem = 0

    if request.session.has_key('phone') :
        phone = request.session['phone']

        totalItem = len(Cart.objects.filter(phone=phone))       
        customer = Customer.objects.filter(phone=phone)
        for c in customer :
            name = c.name 

            order = OrderDetail.objects.filter(user=phone)  
        
            data = {

                'order' : order,
                'name' : name,
                'totalItem' : totalItem
            }

            if order : # Means Ke check kar se user Male che.
                return render(request, 'orders.html',data)
                        
            else :
                # return redirect(f'/cart') 
                return HttpResponse('Not Found value')   
    else :
        return redirect('login_page')
    
# ===============================Search-Bar===================================      

def search(request) :
    totalItem = 0

    if request.session.has_key('phone') :
        phone = request.session['phone']
        query = request.GET.get('query')
        # print(query)

        # If you query with "Nordic Chair", it will match that specific string exactly.
        search = Product.objects.filter(name__iexact = query) # name__contains = query

        totalItem = len(Cart.objects.filter(phone=phone))
        customer = Customer.objects.filter(phone=phone)

        for c in customer :
            name = c.name 
        
        data = {
            'name' : name, 
            'totalItem' : totalItem,
            'search' : search,
            'query' : query,
            'message': None  # Reset message
        }   

        if search.exists(): 
            return render(request, 'search.html', data)
        else:
            # Handle case where no products match
            data['message'] = "No products found."  
            return render(request, 'search.html', data)

    else :
        return redirect('login_page')                  
    
# =============================Payment-Cart=================================      

def payment_cart(request) :    

    if request.method == 'POST' : 
        
        amount = int(request.POST.get('amount')) * 100 
        print(amount)

        # How to create payment Id
        client = razorpay.Client(auth=("rzp_test_bHGARzasqPyY7j","1Ae7bF0U1f1Z9m2FZzD3RhR0"))
        # payment id genrate
        payments = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':1})
        print('payment',payments)
        
        Paymentcart(amount=amount, payment_id = payments["id"]).save()
        
        CartDel = Cart.objects.all()
        CartDel.delete() 
        return render(request, 'payment.html', {'payments':payments}) 
    
    else :
        # Calculate total for each item and the grand total
        cart = Cart.objects.all()
        grand_total = 0 
        for item in cart:
            item.total = item.price * item.quantity
            grand_total += item.total  
        print('grand_total', grand_total)    

        return render(request, 'payment.html', {'grand_total': grand_total})

# =============================Sucess-Message=================================      

@csrf_exempt    
def thankyou_view(request) :
    
    if request.method == 'POST' :
        a = request.POST
        # print(a)
        order_id = ""
        for key, val in a.items() :
            if key == 'razorpay_order_id' :
                order_id = val
                break

        user = Paymentcart.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()    
    return render(request, 'thankyou.html')