from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from django.urls import reverse
from .models import Product,Category,OrderItem,Order
from django.core.paginator import Paginator
from .forms import CartAddForm
from .cart import Cart 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import json


class ProductListView(View):
    def get(self,request):
        products=Product.objects.filter(available=True)
        page_number = request.GET.get("page")
        paginator=Paginator(products,3)
        objects_list=paginator.get_page(page_number) 
        return render(request,'shop/productlist.html',{'products':objects_list})

class CategorytListView(View):
    def get(self,request,category_id):
        category=Category.objects.get(id=category_id)
        products=Product.objects.filter(category=category)
        return render(request,'shop/categorylist.html',{'category':category,'products':products})



class ProductDetailView(View):
    def get(self,request,slug):
        product=get_object_or_404(Product,slug=slug)
        form=CartAddForm()
        context={
            'product':product,
            'form':form

        }
        return render(request,'shop/productdetail.html',context)
        

class CartView(View):
    def get(self,request):
        cart=Cart(request)
        return render(request,'shop/cart.html',{'cart':cart})

class CartAddView(View):
    def post(self,request,product_id):
        cart=Cart(request)
        product=get_object_or_404(Product,id=product_id)
        form=CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product,form.cleaned_data['quantity'])
            return redirect('shop:cart')
    
class CartRemoveView(View):
    def get(self,request,product_id):
        cart=Cart(request)
        product=get_object_or_404(Product,id=product_id)
        cart.remove(product)
        return redirect('shop:cart')


class OrderDetailView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        order=get_object_or_404(Order,id=order_id)
        return render(request,'shop/order.html',{'order':order})



class OrderCreateView(LoginRequiredMixin,View):
    def get(self,request):
        cart=Cart(request)
        order=Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
        cart.clear()
        return redirect('shop:order_detail',order.id)


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000 # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید" # Required
CallbackURL = 'http://localhost:8000/shop/verify/'

class OrderPayView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        order=Order.objects.get(id=order_id)
        request.session['order_pay']={
            'order_id':order.id,
        }

        req_data = {

        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": request.user.phone_number, "email": request.user.email}
        }

        req_header = {"accept": "application/json", "content-type": "application/json'"}

        req = requests.post(url=ZP_API_REQUEST, data=json.dumps( req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")



    

class OrderVerifyView(LoginRequiredMixin,View):
    def get(self,request):
        order_id=request.session['order_pay']['order_id']
        order=Order.objects.get(id=int(order_id))
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json","content-type": "application/json'"}
            req_data = {
                    "merchant_id": MERCHANT,
                    "amount": order.get_total_price(),
                    "authority": t_authority}

            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.paid=True
                    order.save()
                    return HttpResponse('Transaction success.\nRefID: ' + str(req.json()['data']['ref_id']))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(req.json()['data']['message']))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(req.json()['data']['message']))        
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

        else:
            return HttpResponse('Transaction failed or canceled by user')





