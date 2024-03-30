from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Animals,Cart, Address,Order, Order_History, Comments
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import SignUp
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sessions.models import Session
from datetime import timedelta,date,datetime
from razorpay import Client
import uuid
from django.views.decorators.csrf import csrf_exempt
import random
from django.contrib.auth.hashers import make_password


day = timedelta(days=7)
date = date.today()


# Create your views here.

def adminBase(request):
    return render(request,'admin/adminBase.html')

def Admin(request):
    return render(request, 'admin/admin.html')

def AdminForm(request):
    if request.user.is_superuser and request.user.is_authenticated:
        try:
            if request.method == "POST":
                pname = request.POST.get('pname')
                category = request.POST.get('category')
                breed = request.POST.get('breed')
                desc = request.POST.get('desc')
                price = request.POST.get('price')
                image = request.FILES.get('img')
                Animals.objects.create(pname=pname,category=category,breed=breed,desc=desc,price=price,image=image)
                print(image)
            data = Animals.objects.all()
            return render(request,'admin/adminform.html',{'data':data})
        except:
            return HttpResponse("Something Went Wrong")
    else:
        return HttpResponseRedirect('/adminlogin/')
    
def OrderPlace(request,id):
    if request.user.is_authenticated:
        #here we are adding address for order
        try:

            if request.method == "POST":
                name = request.POST.get('name')
                pidd = request.POST.get('opid')
                city = request.POST.get('city')
                pincode = request.POST.get('pincode')
                flat = request.POST.get('flat')
                state = request.POST.get('landmark')
                phone = request.POST.get('phone')
                phone_a = request.POST.get('phone_a')
                if city:
                    user = request.user
                    Address.objects.create(user=user,animals_id=pidd,city=city,pincode=pincode,detail=flat,state=state,cname=name,phone=phone,alternate_phone=phone_a)
                    
                # order fetching from data base
    
            order = Order.objects.all().values_list('animals_id',flat=True)
            if id not in order:
                address = Address.objects.filter(user_id=request.user)
                pid12 = id
                return render(request,'user/orderplace.html',{'pid':pid12, 'address':address})
            else:
                messages.success(request,"This product is already Sold")
                return HttpResponseRedirect('/allanimals/')
        except:
            messages.success(request,"This product is already Sold")
            return HttpResponseRedirect('/allanimals/')
    else:
        return HttpResponseRedirect('/')
    
def Address_del(request,id):
    if request.method == "POST":
        Address.objects.get(pk=id).delete()
        return HttpResponseRedirect('/allanimals/')
        
def Final_order(request):
    if request.user.is_authenticated:
        product_id = 0
        address_id = 0
        Order.objects.create(user=request.user,animals_id=product_id,address_id=address_id)
        return render(request,'user/final_order.html')
    else:
        return HttpResponseRedirect('/')

def Add_To_Cart(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                order = Order.objects.all().values_list('animals_id',flat=True)
                cid = request.POST.get('cid')
                if int(cid) not in order:
                    filter1 = Cart.objects.filter(user_id=request.user).values_list('animals_id',flat=True)
                    print(filter1)
                    if int(cid) not in filter1:
                        Cart.objects.create(animals_id=cid,user=request.user)
                    else:
                        messages.success(request, "This Product is already added in Cart")
                else:
                    messages.success(request,'This product is Sold so You can not add to the add ...')
                    return HttpResponseRedirect('/allanimals/')

            #here we are showing the cart data
            os = Cart.objects.filter(user_id=request.user).values_list('animals_id',flat=True)
            print(list(os))
            all = Animals.objects.filter(id__in=os)
            amount = Animals.objects.filter(id__in=os).values_list('price',flat=True)
            amt=0
            for i in amount:
                amt=amt+i
            
            count = Cart.objects.filter(user_id=request.user).count()
            return render(request,'user/cart.html',{'all':all,'total_amount':amt,'count':count,'ids':list(os)})
        except:
            return HttpResponse("Someething Went Wrong")
    else:
        return HttpResponseRedirect('/login/')
    
def Search(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":
                src = request.POST.get('search')
                print(src)
                all = Animals.objects.filter(Q(pname__icontains=src)|Q(category__icontains=src)|Q(breed__icontains=src)|Q(desc__icontains=src)|Q(price__contains=src))
                print(all)
                count = Cart.objects.filter(user_id=request.user).count()
                print(count)
            return render(request, 'user/search.html',{'data':all,'count':count})
        except:
            return HttpResponseRedirect('/allanimals/')
    else:
        return HttpResponseRedirect('/login/')

    
def UserBase(request):
    if request.user.is_authenticated:
        return render(request, 'user/base.html')
    else:
        return HttpResponseRedirect('/')

def AllAnimals(request):
    if request.user.is_authenticated:
        os = Animals.objects.all()
        count = Cart.objects.filter(user_id=request.user).count()
        order = Order.objects.all()
        uname = request.user
        delivery_date = date + day
        return render(request,'user/allanimals.html',{'os':os,'count':count,'uname':uname, 'delivery_date':delivery_date,'order':order})
    else:
        return HttpResponseRedirect('/')

def Detail(request,id,breed):
    if request.user.is_authenticated:
        detail_data = Animals.objects.filter(pk=id)
        related_pets = Animals.objects.filter(category=breed)[:3:-1]

        #comments fetch

        all_comments = Comments.objects.filter(animals_id=id)

        comment_count = Comments.objects.filter(animals_id=id).count()

        all_comments_user = Comments.objects.filter(animals_id=id).values_list('user_id',flat=True)

        all_users = []
        cnt = []
        i=0
        for uid in all_comments_user:
            
            user = User.objects.filter(id=uid)
            all_users.append(user)
            cnt.append(i)
            i+=1
        print(cnt)

        context = {}
        context['data'] = detail_data
        context['related_pets'] = related_pets
        context['all_comments'] = all_comments
        context['comment_count'] = comment_count
        context['all_users'] = all_users
        context['cnt'] = cnt
        
        
        return render(request, 'user/details.html',context)
    else:
        return HttpResponseRedirect('/')


def SignUp1(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/allanimals/')
    else:
        try:
            if request.method == "POST":
                username = request.POST.get('uname')
                email = request.POST.get('email')
                pass1 = request.POST.get('pass')
                pass2 = request.POST.get('pass1')
                # my_user = User.objects.create_user(username,email,pass1).exists()
                m = User.objects.filter(email=email).exists()
                print(m)

                print("Working....")
                # print(my_user)
                if m:
                    print("Email Already Exist")
                    messages.success(request,'This Gmail Already Register...')
                    return HttpResponseRedirect('/usersignup/')
                else:
                    User.objects.create_user(username,email,pass1)
                    # messages.success(request,'SignUp Successfully...')
                    print("SignUpDone")
                # my_user.save()
                try:
                    subject = f'Welcome {username} To PetStore'
                    message = f'''
                            You have successfully register to pet store 
                                
                            Happy Shoppings...
                            '''
                    email_from = settings.EMAIL_HOST_USER
                    reciepient_list = [email,]
                    print(reciepient_list)
                    send_mail(subject,message,email_from,reciepient_list)
                    return HttpResponseRedirect('/login/')
                except:
                    return HttpResponse("Mail not send")
            return render(request, 'user/signupform.html')
        except:
            return HttpResponseRedirect('/usersignup/')

def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/allanimals/')
    else:
        try:
            if request.method == "POST":
                uname = request.POST.get('uname')
                pass1 = request.POST.get('pass')
                print(uname,pass1)
                user = authenticate(request,username=uname, password=pass1)
                print(uname,pass1)
                print(user)
                if user is not None:
                
                    login(request, user)
                    return HttpResponseRedirect('/allanimals/')
            return render(request,'user/login.html')
        except:
            return HttpResponseRedirect('/usersignup/')
    
def LogOut(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def RemoveCart(request,id):
    if request.user.is_authenticated:
        Cart.objects.filter(animals_id=id).delete()
        return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/')
    
def Pre_Order(request,aid,pid):
    address_id = Address.objects.filter(pk=aid)
    product_id = Animals.objects.filter(pk=pid)
    day = timedelta(days=7)
    date1 = date.today()
    delivery_date = day+date1
    return render(request,'user/pre_order.html',{'aid':address_id,'pid':product_id,'date':delivery_date,'aaid':aid,'ppid':pid})

def Final_order(request,aid,pid):
    if request.user.is_authenticated:
        product_id = aid
        address_id = pid
        Order.objects.create(user=request.user,animals_id=product_id,address_id=address_id)
        return render(request,'user/final_order.html')
    else:
        return HttpResponseRedirect('/')
    
def Order_Confirm(request,aid,pid):
    if request.user.is_authenticated:

        # unique_id = str(uuid.uuid4().hex)[:6:]
        # date1 = datetime.now()
        # datef = date1.strftime('%Y%m%d%H%M%S') 
        # order_id1 = f'PS{datef}-{unique_id}'
        amount1 = Animals.objects.get(pk=pid).price
        print(amount1)
        order_id = Order.objects.all().values_list('animals_id',flat=True)
        cart_id = Cart.objects.all().values_list('animals_id',flat=True)
        print(order_id, cart_id)


        if pid not in order_id:
            # get,create=Order.objects.get_or_create(user=request.user,animals_id=pid,address_id=aid,order_id=order_id1)
            order_id = Order.objects.all().values_list('animals_id',flat=True)
            for i in order_id:
                if i in cart_id:
                    print('Working......')
                    Cart.objects.filter(animals_id__in=order_id).delete()

            client = Client(auth=('rzp_test_nTflZwWcazIDRj','wcZcNPWmFAJRDWGz3FspaHzi'))
            amount = amount1
            data = {"amount":amount,"currency":"INR","receipt":"1"}

            payment = client.order.create(data)

            # order_id_pay = Order.objects.filter(animals_id=pid).values_list('order_id',flat=True)
        
            context = {}
            context['payment']=payment
            context['amt'] = payment['amount']*100
            # context['order_id'] = order_id_pay[0]
            context['amount'] = amount1
            context['aid'] = aid
            context['pid'] = pid

            # if not create:
            #     get.payment = amount1
            #     get.save()

            
        else:
            messages.success(request,'Product Alredy Ordered')
            return HttpResponseRedirect('/allanimals/') 
       
        return render(request, 'user/order_confirm.html', context )
    else:
        return HttpResponseRedirect('/')
    
def Cart_Address(request):
    if request.user.is_authenticated:
        #here we are adding address for order
        if request.method == "POST":
            name = request.POST.get('name')
            # pidd = request.POST.get('opid')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            flat = request.POST.get('flat')
            state = request.POST.get('landmark')
            phone = request.POST.get('phone')
            phone_a = request.POST.get('phone_a')
            if city:
                user = request.user
                Address.objects.create(user=user,city=city,pincode=pincode,detail=flat,state=state,cname=name,phone=phone,alternate_phone=phone_a)
                    
                # order fetching from data base
    
        order = Order.objects.all().values_list('animals_id',flat=True)
        if id not in order:
            address = Address.objects.filter(user_id=request.user)

            return render(request,'user/cart_address.html',{'address':address})
        else:
            messages.success(request,"This product is already Sold")
            return HttpResponseRedirect('/cartaddress/')
    # except:
    # messages.success(request,"This product is already Sold")
    #     return HttpResponseRedirect('/cartaddress/')
    else:
        return HttpResponseRedirect('/')
    

def Cart_Preorder(request,aid):
    # address_id = Address.objects.filter(user_id=request.user)
    day = timedelta(days=7)
    date1 = date.today()
    delivery_date = day+date1
    cart = Cart.objects.filter(user_id=request.user).values_list('animals_id',flat=True)
    # for i in cart:
    print(list(cart))
    address = Address.objects.filter(id=aid)
    animal = Animals.objects.filter(id__in=cart)
    animal_amt = Animals.objects.filter(id__in=cart).values_list('price',flat=True)
    finalamount = sum(animal_amt)
    return render(request,'user/cart_preorder.html',{'date':delivery_date,'data':animal,'addressdata':address,'finalamount':finalamount,'aid':aid})
    
def Cart_OrderConfirm(request,aid):
    if request.user.is_authenticated:
        cart_id = Cart.objects.filter(user_id=request.user).values_list('animals_id',flat=True)
        # unique_id = str(uuid.uuid4().hex)[:6:]
        # date1 = datetime.now()
        # datef = date1.strftime('%Y%m%d%H%M%S') 
        # order_id1 = f'PS{datef}-{unique_id}'

        amount1 = Animals.objects.filter(id__in=cart_id).values_list('price',flat=True)
        amount1 = sum(list(amount1))
        order_id = Order.objects.all().values_list('animals_id',flat=True)
        
        print(order_id, cart_id)

        for  pid in cart_id:

            if pid not in order_id:
                client = Client(auth=('rzp_test_nTflZwWcazIDRj','wcZcNPWmFAJRDWGz3FspaHzi'))
                amount = amount1
                data = {"amount":amount,"currency":"INR","receipt":"1"}

                payment = client.order.create(data)

                order_id_pay = Order.objects.filter(animals_id=pid).values_list('order_id',flat=True)
            
                context = {}
                context['payment']=payment
                context['amt'] = payment['amount']*100
                # context['order_id'] = order_id_pay[0]
                context['amount'] = amount1
                context['aid'] = aid


                # get,create=Order.objects.get_or_create(user=request.user,animals_id=pid,address_id=aid,order_id=order_id1)
                # order_id = Order.objects.all().values_list('animals_id',flat=True)
                # for i in order_id:
                #     if i in cart_id:
                #         print('Working......')
                #         Cart.objects.filter(animals_id__in=order_id).delete()
                
            else:
                messages.success(request,'Product Alredy Ordered')
                return HttpResponseRedirect('/allanimals/') 
       
        return render(request,'user/cartorder_confirm.html',context)
    else:
        return HttpResponseRedirect('/')
    

@csrf_exempt
def CartReal_Order(request,aid):
    if request.user.is_authenticated:
        cart_id = Cart.objects.filter(user_id=request.user).values_list('animals_id',flat=True)
        unique_id = str(uuid.uuid4().hex)[:6:]
        date1 = datetime.now()
        datef = date1.strftime('%Y%m%d%H%M%S') 
        order_id1 = f'PS{datef}-{unique_id}'


        order_id = Order.objects.all().values_list('animals_id',flat=True)
        
        print(order_id, cart_id)

        for  pid in cart_id:

            if pid not in order_id:            
                Order.objects.get_or_create(user=request.user,animals_id=pid,address_id=aid,order_id=order_id1)
                order_id = Order.objects.all().values_list('animals_id',flat=True)
                for i in order_id:
                    if i in cart_id:
                        print('Working......')
                        Cart.objects.filter(animals_id__in=order_id).delete()
                
            else:
                messages.success(request,'Product Alredy Ordered')
                return HttpResponseRedirect('/allanimals/') 
        return render(request,'user/cartfinal.html')
        
    else:
        return HttpResponseRedirect('/')
       

@csrf_exempt   
def Real_Order(request,aid,pid):
    cart_id = Cart.objects.filter(user_id=request.user).values_list('animals_id',flat=True)
    unique_id = str(uuid.uuid4().hex)[:6:]
    date1 = datetime.now()
    datef = date1.strftime('%Y%m%d%H%M%S') 
    order_id1 = f'PS{datef}-{unique_id}'
    amount1 = Animals.objects.filter(id__in=cart_id).values_list('price',flat=True)
    amount1 = sum(list(amount1))
    order_id = Order.objects.all().values_list('animals_id',flat=True)
        
    print(order_id, cart_id)
    day = timedelta(days=7)
    date1 = date.today()
    delivery_date = day+date1
    # for  pid in cart_id:
    if pid not in order_id:
        Order.objects.create(user=request.user,animals_id=pid,address_id=aid,order_id=order_id1,delivery_date=delivery_date)
        order_id = Order.objects.all().values_list('animals_id',flat=True)
        for i in order_id:
            if i in cart_id:
                print('Working......')
                Cart.objects.filter(animals_id__in=order_id).delete()
                
    else:
        messages.success(request,'Product Alredy Ordered')
        return HttpResponseRedirect('/allanimals/')
    return render(request,'user/final.html')

def final(request):
    return render(request,'user/final.html')
    
def Orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user_id=request.user).values_list('animals_id',flat=True)
        ordersdata = Animals.objects.filter(id__in=orders)
        print(ordersdata)
        date = Order.objects.filter(user_id=request.user)
        address = Address.objects.filter(user_id=request.user)
        # day = timedelta(days=7)
        # date1 = date.today()
        # delivery_date = day+date1
        return render(request,'user/orders.html',{'ordersdata':ordersdata,'date':date,'address':address})
    else:
        return HttpResponseRedirect('/login/')
def AdminSignUp(request):
    if request.method == "POST":
        username = request.POST.get('uname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        pass2 = request.POST.get('pass1')
        my_user = User.objects.create_user(username,email,pass1)
        my_user.is_staff = True
        my_user.is_superuser = True
        my_user.save()
        # user.save()
        try:
            subject = f'Welcome {username} To PetStore'
            message = f'''
                    You have successfully register to pet store 
                                
                    Happy Shoppings...
                    '''
            email_from = settings.EMAIL_HOST_USER
            reciepient_list = [email,]
            print(reciepient_list)
            send_mail(subject,message,email_from,reciepient_list)
            return HttpResponseRedirect('/')
        except:
            return HttpResponse("Mail not send")
    return render(request,'admin/adminSignUp.html')


def AdminLogin(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        pass1 = request.POST.get('pass')
        print(uname,pass1)
        user = authenticate(request,username=uname, password=pass1)
        print(uname,pass1)
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/adminform/')
    return render(request,'admin/admin_login.html')
    
def Delivery_Boy(request):
    animals_id = Order.objects.all().values_list('animals_id',flat=True)
    address_id = Order.objects.all().values_list('address_id',flat=True)
    orders = Order.objects.all()
    data = Animals.objects.filter(id__in=animals_id)
    address_data = Address.objects.filter(id__in=address_id)
    oh = Order_History.objects.all()

    return render(request,'delivery/delivery_boy.html',{'data':data,'adata':address_data,'orders':orders,'oh':oh})

def Order_Histories(request,pid,aid):
    if request.user.is_authenticated:
        pet = Animals.objects.get(pk=pid)
        adr = Address.objects.get(pk=aid)
        orderid = Order.objects.get(animals_id=pid)
        print(adr)
        ad = Order.objects.filter(animals_id=pid).values_list('user_id',flat=True)
        userid = list(ad)
        pname = pet.pname
        category = pet.category
        breed = pet.breed
        price = pet.price
        image = pet.image
        user = userid[0]
        cname = adr.cname
        city = adr.city
        pincode = adr.pincode
        detail = adr.detail
        state = adr.state
        phone = adr.phone
        alternate_phone = adr.alternate_phone
        orderid = orderid.order_id
    
        Order_History.objects.create(pname=pname,category=category,
        breed=breed,price=price,image=image,user=user,cname=cname,city=city,detail=detail,
        state=state,phone=phone,alternate_phone=alternate_phone,order_id=orderid)
        Order.objects.get(animals_id=pid).delete()
        return HttpResponseRedirect('/deliveryboy/')
    else:
        return HttpResponseRedirect('/login/')

def Order_Histories_Show(request):
    if request.user.is_authenticated:
        show = Order_History.objects.filter(user=request.user.id)
        context = {}
        context['ohistory'] = show
        return render(request,'user/order_history_show.html',context)
    else:
        return HttpResponseRedirect('/login/')

#Admin Profile Page
def Admin_Profile(request):
    if request.user.is_superuser and request.user.is_authenticated:
        orders1 = Order.objects.all().count()
        order_history = Order_History.objects.all().count()
        all1 = Animals.objects.all().count()
        unsell = all1-orders1
        users = User.objects.all().count()
        animals_id = Order.objects.all().values_list('animals_id',flat=True)
        address_id = Order.objects.all().values_list('address_id',flat=True)
        orders = Order.objects.all()
        data = Animals.objects.filter(id__in=animals_id)
        address_data = Address.objects.filter(id__in=address_id)
        oh = Order_History.objects.all()
        context = {}
        context['orders1'] = orders1
        context['ohistory'] = order_history
        context['unsell'] = unsell
        context['users'] =  users
        context['data'] = data
        context['adata'] = address_data
        context['orders'] = orders
        context['oh'] = oh

        return render(request,'admin/admin_profile.html',context)
    else:
        return HttpResponseRedirect('/adminlogin/')

def IndexPage(request):
    allpets = Animals.objects.all()
    context = {}
    context['allpets'] = allpets 
    return render(request,'user/index.html',context)

def OTP_Generate(request):
    if request.method == 'POST':
      
        email = request.POST.get('mail')
        aa = User.objects.filter(email=email).exists()
        if aa:
            print('Valid')
            otp = ''.join(random.choices('0123456789', k=4))
            otp = int(otp)
            subject = 'OPT Verification For PassWord Chnage'  
            message = f'This is your OTP {otp} valid for next 10 minutes' 
            from1 = settings.EMAIL_HOST_USER
            email1 = email
            send_mail(subject,message,from1,[email1])
            print("Send Email")
            return render(request,'user/passchange.html',{'otp':True}) 

    return render(request,'user/passchange.html')

# def PassowrdChange(request):
#     return render(request,'user/passchange.html')

def Comment(request,id,breed):
    if request.method=="POST":
       cmt = request.POST.get('comment')
       Comments.objects.create(user=request.user,animals_id=id,comment=cmt)
       
    return HttpResponseRedirect(f'/details/{id}/{breed}')