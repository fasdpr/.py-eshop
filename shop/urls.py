from django.urls import path
from . import views

app_name="shop"
urlpatterns = [
    path('products/',views.ProductListView.as_view(),name='product_list'),
    path('categories/<int:category_id>/',views.CategorytListView.as_view(),name='category_list'),

    path('create/',views.OrderCreateView.as_view(),name='create_order'),
    path('detail/<int:order_id>',views.OrderDetailView.as_view(),name='order_detail'),
    path('cart/',views.CartView.as_view(),name="cart"),

    path('<slug:slug>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('cart/add/<int:product_id>/',views.CartAddView.as_view(),name='cart_add'),
    path('cart/remove/<int:product_id>/',views.CartRemoveView.as_view(),name='cart_remove'),
    path('create/',views.OrderCreateView.as_view(),name='create_order'),
    path('detail/',views.OrderDetailView.as_view(),name='order_detail'),
    path('pay/<int:order_id>/',views.OrderPayView.as_view(),name='order_pay'),
    path('verify/',views.OrderVerifyView.as_view(),name='order_verify'),
]
