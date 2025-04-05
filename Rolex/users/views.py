from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Watch
from .forms import *
from .models import Basket, BasketItem, Order, OrderItem


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been  created. You are now able to log in !')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(BasketItem, pk=item_id)
    if item.quantity <= item.product.quantity:
        item.quantity = item.quantity + 1
        item.save()
    return redirect('basket-view')


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(BasketItem, pk=item_id)
    if item.quantity > 1:
        item.quantity = item.quantity - 1
        item.save()
        return redirect('basket-view')
    else:
        return redirect('remove_item', item_id=item.id)


@login_required
def remove_item(request, item_id):
    item = get_object_or_404(BasketItem, pk=item_id)
    product_name = item.product.name
    item.delete()
    messages.success(request, f"Removed {product_name} from your basket")
    return redirect('basket-view')


def cart_view(request):
    items = []
    total_price = 0
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).first()
        items = BasketItem.objects.filter(basket=basket).all() if basket else []
        if items:
            for item in items:
                total_price += item.product.price * item.quantity

    return render(request, 'users/add_to_basket.html', {'items': items, 'total_price': total_price})


@login_required
@transaction.atomic
def process_order(request):
    if request.method != 'POST':
        return redirect("basket-view")

    try:
        with transaction.atomic():
            # Get or create order
            order = Order.objects.create(
                user=request.user,
                status='pending',
                price=0
            )

            basket = get_object_or_404(Basket, user=request.user)
            basket_items = BasketItem.objects.filter(basket=basket)
            order_items = []
            if not basket_items.exists():
                messages.warning(request, "Your basket is empty!")
                return redirect("basket-view")

            total_price = 0
            for basket_item in basket_items:
                # Check stock availability first
                if basket_item.product.quantity < basket_item.quantity:
                    raise ValueError(f"Not enough stock for {basket_item.product.name}")

                # Create order item
                order_item = OrderItem.objects.create(
                    order=order,
                    product=basket_item.product,
                    quantity=basket_item.quantity
                )
                total_price += basket_item.product.price * basket_item.quantity
                order_items.append(order_item)

            # Update order total
            order.price = total_price
            order.save()

            # Clear basket only after successful order creation
            basket_items.delete()

            return render(request, "users/order_confirmation.html", {
                'order': order,
                'order_items': order_items
            })

    except Exception as e:
        messages.error(request, f"Order processing failed: {str(e)}")
        return redirect("basket-view")


@login_required
@transaction.atomic
def confirm_order(request):
    if request.method != "POST":
        return redirect("product-list")

    try:
        with transaction.atomic():
            order = get_object_or_404(
                Order.objects.filter(user=request.user, status='pending'),  # QuerySet first
                pk=Order.objects.filter(user=request.user, status='pending')
                .latest('date').pk  # Get latest PK
            )
            order_items = OrderItem.objects.filter(order=order).all()
            for order_item in order_items:
                product = order_item.product
                if product.quantity < order_item.quantity:
                    raise ValueError(f"Insufficient stock for {product.name}")

                product.quantity -= order_item.quantity
                product.save()

            order.status = 'completed'
            order.save()

            messages.success(request, 'Your order has been confirmed')
            return redirect('order_success', order_id=order.id)

    except Exception as e:
        messages.error(request, f"Confirmation failed: {str(e)}")
        return redirect("order_confirmation")


def history_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        Prefetch('orderitems', queryset=OrderItem.objects.select_related('product'))
    ).order_by('-date')

    return render(request, 'users/order_history.html', {'orders': orders})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order).all()
    return render(request, "users/order_success.html", {
        'order': order,
        'order_items': order_items
    })


@login_required
def cancel_order(request):
    if request.method == "POST":
        order = Order.objects.filter(user=request.user).last()
        order.status = 'cancelled'
        orderItems = OrderItem.objects.filter(order=order).all()
        orderItems.delete()
        messages.success(request, f'Your order has been cancelled')
        return redirect('product-list')


def add_to_basket(request, product_id):
    if not request.user.is_authenticated:
        return render(request, 'users/unauthorized.html', status=401)
    product = get_object_or_404(Watch, id=product_id)
    basket, created = Basket.objects.get_or_create(user=request.user)
    basket_item, item_created = BasketItem.objects.get_or_create(
        product=product,
        basket=basket,
        defaults={'quantity': 1, })

    if not item_created:
        basket_item.quantity += 1
        basket_item.save()

    return redirect("basket-view")


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your changes have been saved!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/profile.html', context=context)
