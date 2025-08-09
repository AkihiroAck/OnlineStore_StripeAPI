import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Item, Order


stripe.api_key = settings.STRIPE_SECRET_KEY


def item_detail(request, id):
    """Отображает детали товара и форму для покупки"""
    item = get_object_or_404(Item, id=id)
    return render(request, 'payments/item.html', {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


def buy_item(request, id):
    """Обрабатывает покупку отдельного товара"""
    item = get_object_or_404(Item, id=id)
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success_buy')),
        cancel_url=request.build_absolute_uri(reverse('cancel_buy')),
    )
    
    return JsonResponse({'session_id': session.id})


def create_order(request):
    """Создает новый заказ"""
    if 'order_id' in request.session:
        return redirect('current_order')
    order = Order.objects.create()
    request.session['order_id'] = order.id
    return order


def add_to_order(request, item_id):
    """Добавляет товар в заказ"""
    item = get_object_or_404(Item, id=item_id)
    
    if 'order_id' not in request.session:
        order = create_order(request)
    else:
        order = Order.objects.get(id=request.session['order_id'])
    
    order.items.add(item)
    return redirect('item_detail', id=item_id)


def remove_from_order(request, item_id):
    """Удаляет товар из заказа"""
    if 'order_id' not in request.session:
        return redirect('current_order')
    
    order = Order.objects.get(id=request.session['order_id'])
    item = get_object_or_404(Item, id=item_id)
    order.items.remove(item)
    
    if order.items.count() == 0:
        order.delete()
        del request.session['order_id']
    
    return redirect('current_order')


def clear_order(request):
    """Очищает заказ полностью"""
    if 'order_id' in request.session:
        try:
            Order.objects.get(id=request.session['order_id']).delete()
            del request.session['order_id']
        except Order.DoesNotExist:
            pass
    return redirect('current_order')


def current_order(request):
    """Отображает текущий заказ"""
    if 'order_id' not in request.session:
        return render(request, 'payments/order.html', {'order': None})
    
    order = Order.objects.get(id=request.session['order_id'])

    return render(request, 'payments/order.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


def buy_order(request, id):
    """Обрабатывает покупку заказа с списком предметов в описании"""
    order = get_object_or_404(Order, id=id)
    
    items_list = ", ".join([item.name for item in order.items.all()])
    items_description = f"Items: {items_list}" if items_list else "Empty order"

    subtotal = sum(item.price for item in order.items.all())
    total = order.get_total_price()
    
    line_item = {
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': f'Order #{order.id}',
                'description': (
                    f"{items_description}\n| "
                    f"Subtotal: ${subtotal:.2f}\n"
                    f"Discount: {order.discount.percent_off if order.discount else 0}%\n"
                    f"Tax: {order.tax.percentage if order.tax else 0}%"
                )
            },
            'unit_amount': int(total * 100),
        },
        'quantity': 1,
    }
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[line_item],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success_buy')),
        cancel_url=request.build_absolute_uri(reverse('cancel_buy')),
    )
    
    return JsonResponse({'session_id': session.id})


def success_buy(request):
    """Отображает страницу успешной покупки"""
    if 'order_id' in request.session:
        del request.session['order_id']
    return render(request, 'payments/success_buy.html')


def cancel_buy(request):
    """Отображает страницу отмены покупки"""
    if 'order_id' in request.session:
        del request.session['order_id']
    return render(request, 'payments/cancel_buy.html')
