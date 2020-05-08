from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from carts.forms.cart_items_form import CartItemsForm
from carts.forms.payment_form import PaymentForm
from carts.forms.shipping_form import ShippingForm
from main.models import Product
from carts.models import Cart, CartItems, PaymentInformation, ShippingInformation, Order
from users.models import Profile
from django.views.decorators.csrf import csrf_exempt



def index(request):
    context = get_models(request)
    return render(request, 'carts/index.html', context)


@csrf_exempt
def update_cart_items(request):
    if request.is_ajax():
        item_id = int(request.POST.get('id'))
        item_quantity = int(request.POST.get('quantity'))

        if request.user.is_authenticated:

            user_id = Profile.objects.filter(user=request.user).first().id
            user_cart = Cart.objects.filter(userID=user_id).first()
            user_cart_items = CartItems.objects.filter(cartID=user_cart.id, productID=item_id).first()
            user_cart_items.quantity = item_quantity
            user_cart_items.save()

        else:
            for x in range(len(request.session['cart'])):
                if request.session['cart'][x]['id'] == item_id:
                    request.session['cart'][x]['quantity'] = item_quantity

        request.session.save()
        return HttpResponse("success")


def input_shipping_info(request):
    context = get_models(request)

    if request.method == "POST":
        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():

            the_id = None
            all_shipping_info = ShippingInformation.objects.all()
            for info in all_shipping_info:
                if info.last_name == request.POST['last_name'] and \
                        info.first_name == request.POST['first_name'] and \
                        info.city == request.POST['city'] and \
                        info.postcode == int(request.POST['postcode']) and \
                        info.address_2 == request.POST['address_2'] and \
                        info.address_1 == request.POST['address_1'] and \
                        info.country == request.POST['country']:
                    the_id = info.id
                    print(info)
                    print(info.id)
                    print("DUPE")
                    break

            if the_id == None: #<----- if NOT duplicate
                form_instance = shipping_form.save(commit=False)
                the_id = form_instance.id
                print(the_id)
                form_instance.save()

            return redirect('payment_info', the_id)




    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        shipping_info = ShippingInformation.objects.filter(id=profile.shipping_information_id.id).first()

    else:
        shipping_info = ShippingInformation()



    context['shipping_info_form'] = ShippingForm(instance=shipping_info)

    return render(request, 'carts/shipping_info.html', context)

def input_payment_info(request, id):

    if request.method == "POST":
        payment_form = PaymentForm(data=request.POST)
        if payment_form.is_valid():
            print("IS WALDO")
            the_id = None
            all_payment_info = PaymentInformation.objects.all()
            for info in all_payment_info:
                print(info.expiration_date, request.POST['expiration_date'])
                if info.last_name == request.POST['last_name'] and \
                        info.first_name == request.POST['first_name'] and \
                        info.card_number == request.POST['card_number'] and \
                        info.expiration_date == int(request.POST['expiration_date']) and \
                        info.cvv == request.POST['ccv']:
                    the_id = info.id
                    print(info)
                    print(info.id)
                    print("DUPE")
                    break

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        payment_info = PaymentInformation.objects.filter(id=profile.shipping_information_id.id).first()

    else:
        payment_info = PaymentInformation()

    context = get_models(request)

    context['payment_info_form'] = PaymentForm(instance=payment_info)
    return render(request, 'carts/payment_info.html', context)


def cart_add(request, id):
    product = Product.objects.filter(id=id).first()

    if request.user.is_authenticated:
        user_id = Profile.objects.filter(user=request.user).first().id
        user_cart = Cart.objects.filter(userID=user_id).first()
        if not user_cart:
            user_cart = Cart.objects.create(userID=user_id, check_out=False)
        cart_items = CartItems.objects.filter(cartID=user_cart.id, productID=product.id)
        if len(cart_items) != 0:
            first_item = cart_items.first()
            first_item.quantity += 1
            first_item.save()
        else:
            CartItems.objects.create(productID=product.id, quantity=1, cartID=user_cart, price=product.price)

    else:
        duplicate = False
        if 'cart' not in request.session.keys():
            request.session['cart'] = []
        for x in range(len(request.session['cart'])):
            if request.session['cart'][x]['id'] == product.id:
                request.session['cart'][x]['quantity'] += 1
                duplicate = True

        if not duplicate:
            request.session['cart'].append({
                'name': product.name,
                'price': product.price,
                'img': product.product_display_image,
                'quantity': 1,
                'id': product.id
            })
        request.session.save()

    return redirect(request.GET['next'])

@csrf_exempt
def remove_product(request):
    if request.is_ajax():
        product_id = int(request.POST.get("id"))
        if request.user.is_authenticated:
            user_id = Profile.objects.filter(user=request.user).first().id
            user_cart_id = Cart.objects.filter(userID=user_id).first().id
            product = CartItems.objects.filter(cartID=user_cart_id, productID=product_id).first()
            product.delete()
        else:
            for x in range(len(request.session['cart'])):
                if request.session['cart'][x]['id'] == product_id:
                    request.session['cart'].pop(x)
                    break
            request.session.save()

        return HttpResponse("success")

@csrf_exempt
def clear_cart(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = Profile.objects.filter(user=request.user).first().id
            user_cart = Cart.objects.filter(userID=user_id).first()
            user_cart.delete()
        else:
            request.session.clear()
            request.session.save()

        return HttpResponse("success")


def get_models(request):
    class Model:
        name = ""
        quantity = 0
        img = ""
        price = 0
        id = 0

    models = []
    price_sum = 0
    if request.user.is_authenticated:
        user_id = Profile.objects.filter(user=request.user).first().id
        user_cart = Cart.objects.filter(userID=user_id).first()
        if user_cart:
            cart = CartItems.objects.filter(cartID=user_cart.id)
            for product in cart:
                model = Model()
                model.quantity = product.quantity
                model.price = product.price * product.quantity
                model.id = product.productID
                item = Product.objects.filter(id=product.productID).first()
                price_sum += product.price * product.quantity
                model.img = item.product_display_image
                model.name = item.name
                models.append(model)

    else:
        if "cart" in request.session.keys():
            for product in request.session['cart']:
                model = Model()
                model.quantity = product['quantity']
                model.price = product['price'] * product['quantity']
                price_sum += product['price'] * product['quantity']
                model.img = product['img']
                model.name = product['name']
                model.id = product['id']
                models.append(model)

    context = {
        'price_sum': price_sum,
        'products': models
    }

    return context
