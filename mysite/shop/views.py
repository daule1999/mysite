from django.shortcuts import render, redirect
from .models import Product, Contact , Orders
from math import ceil
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def signin(request):
    return render(request, 'shop/signin.html')

def index(request):
    #products = Product.objects.all()
    #print(products)
    #n = len(products)
    #nSlides= (n//4) + ceil((n/4)-(n//4))
    #params = {'no_of_slide': nSlides,'range':range(1,nSlides),'product': products}

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = (n // 4) + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    #params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    #allProds = [[products, range(1, nSlides), nSlides],
      #           [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds}
    return render(request,'shop/index.html' , params)

def search(request):
    return render(request,'shop/about.html')

def tracker(request):
    return HttpResponse("We are tracker")

def contact(request):
    if request.method=="POST":

        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request,'shop/contact.html')
def prodview(request,myid):
    #fetch the producut using id
    product = Product.objects.filter(id=myid)
    return render(request,'shop/prodview.html',{'product': product[0]})
def about(request):
    return render(request,'shop/about.html')
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')

def handlesignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check error in params
        if len(username) > 10:
            messages.error(request, " username must be less than 10 character")
            return redirect('/shop/signin')

        if not username.isalnum():
            messages.error(request, " username should only contain letters and numbers")
            return redirect('/shop/signin')
        if pass1 != pass2:
            messages.error(request, " Password do not match")
            return redirect('/shop/signin')


        # create user

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        messages.success(request, " Your Account is creates Successfully")
        return redirect('/shop')
    else:
        return HttpResponse('404 - Not Found')


def handlelogin(request):

    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request, "Successfully Logged In")
            return redirect('/shop')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/shop/signin')

    return HttpResponse('404 - Not Found')


def handlelogout(request):
    logout(request)
    messages.success(request, " Successfully logged out")
    return redirect('/shop')

