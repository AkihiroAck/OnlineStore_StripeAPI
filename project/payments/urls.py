from django.urls import path
from .views import item_detail, buy_item, buy_order, add_to_order, create_order, current_order, remove_from_order, clear_order, success_buy, cancel_buy

urlpatterns = [
    path('item/<int:id>/', item_detail, name='item_detail'),  # Отображение товара
    path('buy/<int:id>/', buy_item, name='buy_item'),  # Покупка отдельного товара
    path('order/add/<int:item_id>/', add_to_order, name='add_to_order'),  # Добавление товара в заказ
    path('order/remove/<int:item_id>/', remove_from_order, name='remove_from_order'),  # Удаление товара из заказа
    path('order/clear/', clear_order, name='clear_order'),  # Очистка заказа
    path('order/create/', create_order, name='create_order'),  # Создание нового заказа
    path('order/current/', current_order, name='current_order'),  # Отображение текущего заказа
    path('buy_order/<int:id>/', buy_order, name='buy_order'),  # Обработка покупки всего заказа
    path('success/', success_buy, name='success_buy'),  # Успешная покупка
    path('cancel/', cancel_buy, name='cancel_buy'),  # Отмена покупки
]
