from .cart import Cart

def cart(request):
    return {'cart_key':Cart(request)}