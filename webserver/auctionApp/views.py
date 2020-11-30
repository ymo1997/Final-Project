from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render
from datetime import timedelta, datetime
from .forms import *
from django.utils import timezone
import requests

URL_BASE = "http://127.0.0.1:5000/"
categories = ["fashion", "electronics", "motors", "collectibles", "home",
              "sporting goods", "toys", "business", "music", "industrial"]
# Create your views here.

User = get_user_model()

def get_shopping_cart(request):
    if "user" not in request.session:
        return []
    user_id = request.session["user"].get("user_id")
    r = requests.get(URL_BASE +
                     "shopping-cart/list-user-shopping-cart-items" +
                     "?user_id={}".format(user_id))
    if r is None or type(r.json()) is str:
        return redirect('home')
    item_list = r.json()["item_list"]
    cart = []
    for item_id in item_list:
        res = requests.post(URL_BASE + "item/get-item-info",
                            json={"item_id": item_id})
        if res is None:
            print("ERROR: ITEM ID is invalid.")
            continue
        res_dict = res.json()
        cart.append({
            'item_name': res_dict.get("item_name"),
            'image_url': res_dict.get("image_url"),
            'current_price': res_dict.get("current_auction_price"),
            'category': res_dict.get("category_name"),
            'shipping_cost': res_dict.get("shipping_cost"),
        })
    request.session["user"]["cart_count"] = len(cart)
    request.session["user"]["cart"] = cart
    return cart

def register(request):
    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        account_type = request.POST.get("account_type")
        if password1 == password2:
            r = requests.post(URL_BASE + "login/register",
                              json = {"first_name": f_name,
                                      "last_name": l_name,
                                      "email": email,
                                      "password": password1,
                                      "is_admin": account_type == "Admin"})
            print("DEBUG: STATUS CODE {}".format(r.status_code))
            if r.status_code == 400:
                messages.info(request, 'Email Taken')
                return HttpResponseRedirect(reverse('register'))
            elif r.status_code == 200:
                res = r.json()
                request.session['user'] = {"email": email,
                                           "user_id": res.get("_id"),
                                           "is_admin": account_type == "Admin"}
                request.session['login'] = True
                return redirect(reverse('home'))
            else:
                return HttpResponseRedirect(reverse('register'))
        else:
            messages.info(request, 'Password not matching')
            return HttpResponseRedirect(reverse('register'))

    else:
        return render(request, 'signup.html', {'page': 'signup', 'login': request.session.get('login')})


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        next_url = request.GET.get("next")
        print("next: {}".format(next_url))
        r = requests.post(URL_BASE + "login/login",
                          json = {"email": email, "password": password})
        print("DEBUG: status_code : {}".format(r.status_code))
        if r is None:
            return redirect(reverse('home'))
        r_dict = r.json()
        if r.status_code == 200:
            # auth.login(request, user)
            res_dict = r.json()
            request.session['login'] = True
            request.session['user'] = {"email": email,
                                       "user_id": r_dict["_id"],
                                       "is_admin": res_dict.get("is_admin")}
            if next_url:
                return redirect(next_url)
            return redirect(reverse('home'))
        else:
            messages.info(request, 'Username or password incorrect')
            return redirect('login')
    else:
        return render(request, 'login.html', {'page': 'login', 'login': request.session.get('login')})

def edit_profile(request):
    if "login" not in request.session or "user" not in request.session or \
       request.session['login'] != True:
        return redirect('login')
    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.info(request, 'Password not matching')
            return HttpResponseRedirect(reverse('edit_profile'))
        user_id = request.session['user']["user_id"]
        payload = {
            "account_id": user_id,
            "email": email,
            "first_name": f_name,
            "last_name": l_name,
            "password": password1
        }
        print(payload)
        r = requests.post(URL_BASE + "user/update-account-info", json = payload)
        print("DEBUG: STATUS CODE {}".format(r.status_code))
        if r.status_code == 400:
            messages.info(request, 'Email Taken')
            return HttpResponseRedirect(reverse('register'))
        elif r.status_code == 200:
            request.session['user']['email'] = email
            return redirect(reverse('home'))
    get_shopping_cart(request)
    return render(request, "edit-profile.html",
                  {
                      "login": request.session['login'],
                      "user": request.session['user'] 
                  })

def user_delete(request):
    if "user" not in request.session:
        return redirect("home")
    is_admin = request.session["user"].get("is_admin")
    user_id = request.session["user"].get("user_id")
    if is_admin:
        if request.method == 'POST':
            email = request.POST.get("email")
            r = requests.post(URL_BASE + "admin/delete-user-account",
                            json = {"email": email}) 
            if r is None or r.status_code != 200:
                print("DEBUG: delete user account failed")
            else:
                return redirect("home")
        return render(request, "deleteuser.html",
                      {
                        "login": request.session['login'],
                        "user": request.session['user'] 
                      })
    else:
        r = requests.post(URL_BASE + "user/delete-account",
                          json = {"account_id": user_id})
        if r is None:
            print("DEBUG: delete user failed.")
        del request.session['user']
        del request.session['login']
        return redirect(reverse('login'))

def user_suspend(request):
    if "user" not in request.session:
        return redirect("home")
    is_admin = request.session["user"].get("is_admin")
    user_id = request.session["user"].get("user_id")
    if is_admin:
        if request.method == 'POST':
            email = request.POST.get("email")
            r = requests.post(URL_BASE + "admin/suspend-user-account",
                            json = {"email": email}) 
            if r is None or r.status_code != 200:
                print("DEBUG: suspend user account failed")
            else:
                return redirect("home")
        return render(request, "suspenduser.html",
                      {
                        "login": request.session['login'],
                        "user": request.session['user'] 
                      })
    else:
        r = requests.post(URL_BASE + "user/suspend-account",
                          json = {"account_id": user_id})
        if r is None:
            print("DEBUG: suspend user failed.")
        request.session.pop('user', None)
        request.session.pop('login', None)
        return redirect(reverse('login'))

def stopauction(request):
    item_id = request.GET.get('item_id')
    print(item_id)
    r = requests.get(URL_BASE + "item/stop-item-auction" +
                    "?item_id=" + item_id)
    if r is None or r.status_code != 200:
        print("DEBUG: stop auction failed")
    return redirect("home")
    


def user_logout(request):
    auth.logout(request)
    request.session.pop('user', None)
    request.session.pop('login', None)
    return redirect(reverse('login'))

def home(request):
    # home info 
    res = requests.post(URL_BASE + "item/list-items", json={})
    items = []
    if res is not None:
        res_dict = res.json()
        print(res_dict)
        for item in res_dict["item_list"]:
            temp = {}
            image_url = item.get("image_url")
            if image_url and image_url != "None":
                temp["url"] = image_url
            else:
                temp["url"] = "https://www.flaticon.com/svg/static/icons/svg/743/743007.svg"
            temp["item_name"] = item.get("item_name")
            temp["current_price"] = item.get("starting_price")
            temp["category"] = item.get("category_name")
            temp["slug"] = item.get("item_id")
            items.append(temp)
    if 'user' in request.session:
        user_info = request.session['user']
    else:
        user_info = None
    context = {
        'items':items,
        'categories':[],
        'page':'home',
        'login': request.session.get('login'),
        'user': user_info
    }
    get_shopping_cart(request)
    return render(request, 'home.html', context)


def createProduct(request):
    if "login" not in request.session or "user" not in request.session or \
       request.session['login'] != True:
        return redirect('login')
    if request.method == 'POST':
        start = request.POST.get("start")
        end = request.POST.get("cap_time")
        start_dt = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end_dt = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        payload = {}
        user_id = request.session["user"].get('user_id')
        if user_id is None:
            return redirect('login')
        payload["description"] = request.POST.get("item_description")
        payload["item_name"] = request.POST.get("item_name")
        payload["condition"] = int(request.POST.get("condition"))
        payload["seller_id"] = user_id
        payload["starting_price"] = request.POST.get("base_price")
        payload["auction_start_time"] = int(start_dt.timestamp())
        payload["auction_end_time"] = int(end_dt.timestamp())
        payload["category_id"] = int(request.POST.get('item_category'))
        payload["shipping_cost"] = int(float(request.POST.get("shipping_cost")))
        image = request.FILES.get('image')
        if image:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            payload["image_url"] = uploaded_file_url
        print(payload)
        r = requests.post(URL_BASE + "item/create-item", json=payload)
        if r.status_code == 200:
            res = r.json()
            item_id = res.get("item_id")
    form1 = ItemForm()
    form2 = AuctionForm()
    context = {
        'form1': form1,
        'form2': form2,
        'page':'sell',
        'cart': [],
        'login': request.session.get('login')
    }
    get_shopping_cart(request)
    return render(request, 'productForm.html', context)

def detail(request, slug):
    if "login" not in request.session or request.session['login'] != True:
        return redirect('login')
    res = requests.post(URL_BASE + "item/get-item-info", json={"item_id": slug})
    if res is None:
        return redirect('home')
    res_dict = res.json()
    print(res_dict)
    status = ""
    if res_dict["status"] == "on-going":
        status = "live"
    elif res_dict["status"] == "ready":
        status = "upcoming"
    r = requests.post(URL_BASE + "login/get-account-info",
            json={"account_id": res_dict["seller_id"]})
    r_dict = r.json()
    print(r_dict)
    if res_dict["current_auction_price"] is not None:
        show_price = res_dict["current_auction_price"]
    else:
        show_price = res_dict["starting_price"] 
    # process time
    start_epoch_time = res_dict["auction_start_time"]
    start_dt = None
    if start_epoch_time is not None:
        start_dt = datetime.fromtimestamp(start_epoch_time)     
    end_epoch_time = res_dict["auction_end_time"]
    end_dt = None
    if end_epoch_time is not None:
        end_dt = datetime.fromtimestamp(end_epoch_time)  
    
    if "image_url" in res_dict:
        urls = [res_dict['image_url']]
    else:
        urls = ["/media/item_images/product-01.jpg"]
    print(status)
    context = {
        'item': {
            "category": res_dict["category_name"],
            "item_name": res_dict["item_name"],
            "current_price": show_price,
            "auction_status": status,
            "slug": slug,
            "start_time": start_dt,
            "end_time": end_dt,
            "condition": str(res_dict["condition"]),
            "auction_status": status
        },
        'seller': {"first_name": r_dict.get("first_name"),
                   "last_name": r_dict.get("last_name"),
                   "image": {"url": "/media/profile_images/profilepic.jpg"}},
        'urls': urls,
        'page':'shop',
        'login': request.session.get('login'),
        'user': request.session.get('user')
    }
    if request.user.is_authenticated:
        context['cart'] = Item.objects.filter(buyer=request.user)
    get_shopping_cart(request)
    return render(request, 'product-detail.html', context)


def room(request, slug):
    if "login" not in request.session or request.session['login'] != True:
        return redirect('login')
    res = requests.post(URL_BASE + "item/get-item-info", json={"item_id": slug})
    if res is None:
        return redirect('home')
    res_dict = res.json()
    print(res_dict)
    status = ""
    if res_dict["status"] == "on-going":
        status = "live"
    elif res_dict["status"] == "ready":
        status = "upcoming"
    r = requests.post(URL_BASE + "login/get-account-info",
            json={"account_id": res_dict["seller_id"]})
    r_dict = r.json()
    print(r_dict)
    if res_dict["current_auction_price"] is not None:
        show_price = res_dict["current_auction_price"]
    else:
        show_price = res_dict["starting_price"] 
    # process time
    start_epoch_time = res_dict["auction_start_time"]
    start_dt = None
    if start_epoch_time is not None:
        start_dt = datetime.fromtimestamp(start_epoch_time)     
    end_epoch_time = res_dict["auction_end_time"]
    end_dt = None
    if end_epoch_time is not None:
        end_dt = datetime.fromtimestamp(end_epoch_time)  
    
    if "image_url" in res_dict:
        url = res_dict['image_url']
    else:
        url = "/media/item_images/product-01.jpg"
    item = {
        "category": res_dict["category_name"],
        "item_name": res_dict["item_name"],
        "base_price": show_price,
        "auction_status": status,
        "slug": slug,
        "condition": str(res_dict["condition"]),
        "auction_status": status,
        "url": url,
        "buyer": res_dict.get("current_auction_buyer_id")
    }
    get_shopping_cart(request)
    return render(request, 'auction.html', {
        'room_name': slug,
        'item': item,
        'deadline': end_dt,
        'cart': [],
        'seller': {"id": res_dict["seller_id"],
                   "first_name": r_dict["first_name"],
                   "last_name": r_dict["last_name"],
                   "email": r_dict["email"],
                   "date_joined": r_dict["date_joined"],
                   "image": {"url": "/media/profile_images/profilepic.jpg"}},
        'login': request.session.get('login'),
        'user':  request.session.get('user')
    })


def my_selling_items(request):
    if "login" not in request.session or \
       "user" not in request.session or \
       request.session['login'] != True:
        return redirect('login')
    remove_id = request.GET.get('remove_id')
    if remove_id is not None:
        print("DEBUG: remove ID {}".format(remove_id))
        print(int(remove_id))
        r = requests.post(URL_BASE + "item/delete-item",
                          json = {"item_id": int(remove_id)})
        if r.status_code != 200:
            return redirect('home')
    user_id = request.session["user"].get("user_id")
    if user_id is None:
        return redirect('login')
    res = requests.post(URL_BASE + "item/list-user-sell-items",
                        json = {"user_id": user_id})
    if res is None:
        return redirect('home')
    res_dict = res.json()
    products = []
    for item in res_dict["item_list"]:
        current_price = item.get("starting_price")
        if item.get("current_auction_price") is not None:
            current_price = item.get("current_auction_price") 
        products.append({"item_name": item.get("item_name"),
                         "current_price": current_price,
                         "category": item.get("category_name"),
                         "image_url": item.get("image_url"),
                         "item_id": item.get("item_id")})
    get_shopping_cart(request)
    return render(request, 'my-selling-items.html',
                 {'products':products,
                  'page':'sell',
                  'login': request.session.get('login'),
                  'user': request.session.get('user')})

def shop(request):
    query = request.GET.get("q")
    items = []
    if not query:
        return redirect("home")
    r1 = requests.get(URL_BASE + "search/search-item-by-keyword?keyword=" + query)
    if r1 is not None:
        r1_dict = r1.json()
        item_list1 = r1_dict.get("item_list")
        items.extend(item_list1)
    try: 
        category_id = categories.index(query.lower()) + 1
    except ValueError:
        pass
    else:
        r2 = requests.get(URL_BASE +
                          "search/search-item-by-category" +
                          "?category_id={}".format(category_id))
        r2_dict = r2.json()
        item_list2 = r2_dict.get("item_list")
        exist_ids = list(map(lambda x:x["item_id"], items))
        for item in item_list2:
            if item["item_id"] not in exist_ids:
                items.append(item)
    print("DEBUG: items {}".format(items))
    context = {
        'items': items,
        'query':query,
        'page':'shop',
        'login': request.session.get('login'),
        'user': request.session.get('user')
    }
    get_shopping_cart(request)
    return render(request, "product.html", context)


def cart(request):
    if "login" not in request.session or \
       "user" not in request.session or \
       request.session['login'] != True:
        return redirect('login')
    checkout_user_id = request.GET.get("checkoutuserid")
    print("DEBUG: checkout_user_id {}".format(checkout_user_id))
    ## checkout shopping cart
    if checkout_user_id is not None:
        r = requests.get(URL_BASE + "shopping-cart/checkout-shopping-cart" +
                        "?user_id={}".format(checkout_user_id))
        if r is None or r.status_code != 200:
            print("DEBUG: checkout failed.")
    cart = get_shopping_cart(request)
    context = {
        'cart': cart,
        'page':'cart',
        'login': request.session.get('login'),
        'user': request.session.get('user')
    }
    return render(request, "cart.html", context)

def profile(request):
    if "login" not in request.session or request.session['login'] != True:
        return redirect('login')
    print(request.session['user'])
    res = requests.post(URL_BASE + "login/get-account-info",
                      json={"account_id": request.session['user']["user_id"]})
    res_dict = res.json()
    context = {
        'user' : {"first_name": res_dict.get("first_name"),
                  "last_name": res_dict.get("last_name"),
                  "email": res_dict.get("email"),
                  "date_joined": res_dict.get("date_joined"),
                  "image": {"url": "/media/profile_images/profilepic.jpg"}
                  },
        "object_list" : None,
        'categories':[],
        'items':None,
        'pages': 1,
        'current': int(1),
        'login': request.session['login']
    }
    get_shopping_cart(request)
    return render(request,"profile.html", context)

