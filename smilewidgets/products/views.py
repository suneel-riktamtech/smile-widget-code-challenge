from django.shortcuts import render
import json
from django.http.response import HttpResponse
from products.models import ProductPrice, GiftCard, Product
import datetime
import traceback

# Create your views here.
def getPrice(request):
    try:
        date_submitted = request.GET.get('date', None)
        datetime_obj = datetime.datetime.strptime(date_submitted, '%d-%m-%Y').date()
        productCode = request.GET.get('productCode', None)
        giftCardCode = request.GET.get('giftCardCode', None)
        gift_card = GiftCard.objects.filter(code=giftCardCode)
        products = Product.objects.filter(code=productCode)        
        product_price = ProductPrice.objects.all()        
        if not product_price.exists():
            return HttpResponse(
                json.dumps({'error':"No product found with given product code."}),
                content_type="application/json",status=404)
        else:
                    
            if gift_card.exists():
                gift_card = gift_card[0]
                if validateGiftCard(gift_card, datetime_obj):
                    gift_amount = gift_card.amount
                    return HttpResponse(
                        json.dumps({'product_price':
                        product_price[0].getPrice(datetime_obj),
                        "gift_amount":gift_amount}),
                        content_type="application/json",status=200)
            else:                
                return HttpResponse(
                    json.dumps({'product_price':
                    product_price[0].getPrice(datetime_obj)}),
                    content_type="application/json",status=200)            
            
    except Exception:
        print(traceback.format_exc())
        return HttpResponse(
                json.dumps({'error':"Unable to process the request."}),
                content_type="application/json",status=404)    

def validateGiftCard(giftcard, date):
    date_start = giftcard.date_start
    if not giftcard.date_end:
        date_end = datetime.date(2099, 12, 31)
    else:
        date_end = giftcard.date_end
    if date_start <= date and date <= date_end:
        return True
    else:
        return False