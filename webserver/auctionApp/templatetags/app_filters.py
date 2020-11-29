  
from django.template.defaulttags import register
from auctionApp.models import *

@register.filter
def get_dict_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def image_url_replace(url):
    if url == "None":
        return 'https://www.flaticon.com/svg/static/icons/svg/743/743007.svg'
    return url

@register.filter
def get_item(items, id):
    return Items.objects.get(id=id)

@register.filter()
def get_range(min=5):
    return range(1,int(min)+1)


@register.filter()
def subtotal(cart):
    sum = 0
    for item in cart:
        sum += item["current_price"]
    return sum

@register.filter()
def shipping_cost(cart):
    sum = 0
    for item in cart:
        sum += item["shipping_cost"]
    return sum

@register.filter()
def total(cart):
    sum = 0
    for item in cart:
        sum += item["current_price"] + item["shipping_cost"]
    return sum
    