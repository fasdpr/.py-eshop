from django.shortcuts import render
from django.views import View
from shop.models import Product,Category
from django.core.paginator import Paginator

class HomeView(View):
    def get(self,request):
        products=Product.objects.filter(available=True)
        page_number = request.GET.get("page")
        paginator=Paginator(products,1)
        objects_list=paginator.get_page(page_number) 

        categories=Category.objects.all()
       
        context={
            'products':objects_list,
            'categories':categories
        }
        return render(request,'home/home.html',context)

class AboutView(View):
    def get(self,request):

        return render(request,'home/about.html')

class ContactView(View):
    def get(self,request):

        return render(request,'home/contact.html')

class SearchView(View):
    def get(self,request):
        search=request.GET.get('searchboxx')
        products= Product.objects.filter(name__icontains=search)|Product.objects.filter(description__icontains=search)
        return render(request,'home/search.html',{'products':products})


