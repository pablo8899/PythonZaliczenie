from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from app.forms import CustomUserCreationForm
from app.models import Product, UserProfile
from django.http import JsonResponse

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logged_out.html'
    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST':
            return redirect(reverse_lazy('home'))
        
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

class RegisterView(UserPassesTestMixin, FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save() 

        birthdate = form.cleaned_data.get('birthdate')
        user_profile = UserProfile.objects.create(user=user, birthdate=birthdate)
       
        return super().form_valid(form)
    
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)
    

class HomePageView(TemplateView):
    template_name = 'home.html'

class ProductListView(TemplateView):
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        cart = self.request.session.get('cart', {})

        total_price = 0
        for product_id, product in cart.items():
            total_price += product['price'] * product['quantity']

        context = {
            'cart': cart,
            'total_price': total_price
        }
        return context
    
def remove_from_cart(request, product_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart

    return JsonResponse({'status': 'success', 'message': 'Item removed', 'cart': cart})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url if product.image else None,
            'quantity': 1,
        }

    request.session['cart'] = cart
    return JsonResponse({'status': 'success', 'message': 'Item added to cart', 'cart': cart})

def update_cart_quantity(request, product_id, quantity):
    if 'cart' in request.session:
        cart = request.session['cart']
        if str(product_id) in cart and quantity > 0:
            cart[str(product_id)]['quantity'] = quantity
            request.session['cart'] = cart
            return JsonResponse({'status': 'success', 'message': 'Quantity updated', 'cart': cart})
    
    return JsonResponse({'status': 'error', 'message': 'Product not found in cart or invalid quantity'})

def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return JsonResponse({'status': 'error', 'message': 'Your cart is empty.'})

        total_price = 0
        order_items = []

        for product_id, product in cart.items():
            total_price += product['price'] * product['quantity']
            order_items.append({
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': product['quantity'],
                'image': product.get('image', None),
            })

        new_order = {
            'items': order_items,
            'status': 'Pending',
            'total_price': total_price,
            'date': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        }
        orders = request.session.get('orders', [])
        
        orders.append(new_order)

        request.session['orders'] = orders

        request.session['cart'] = {}

        return JsonResponse({'status': 'success', 'message': 'Order placed successfully!'})

import xml.etree.ElementTree as ET
from django.http import HttpResponse
from datetime import datetime

def export_orders_to_xml(request):
    orders = request.session.get('orders', [])
    
    if not orders:
        return HttpResponse("No orders available to export.", status=404)

    root = ET.Element("orders")

    for order in orders:
        order_elem = ET.SubElement(root, "order")
        
        ET.SubElement(order_elem, "status").text = order.get('status', 'Pending')
        ET.SubElement(order_elem, "total_price").text = str(order.get('total_price', 0.0))
        ET.SubElement(order_elem, "date").text = order.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        items_elem = ET.SubElement(order_elem, "items")
        
        for item in order['items']:
            item_elem = ET.SubElement(items_elem, "item")
            ET.SubElement(item_elem, "id").text = str(item['id'])
            ET.SubElement(item_elem, "name").text = item['name']
            ET.SubElement(item_elem, "price").text = str(item['price'])
            ET.SubElement(item_elem, "quantity").text = str(item['quantity'])

    tree = ET.ElementTree(root)

    response = HttpResponse(content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="orders.xml"'

    tree.write(response, encoding='utf-8', xml_declaration=True)

    return response

class OrdersView(TemplateView):
    template_name = 'orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.request.session.get('orders', [])
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context