# OnlineStore_StripeAPI

Проект реализует API и простейший интерфейс для покупки товаров с помощью Stripe Checkout.
Поддерживается как покупка отдельных товаров, так и составных заказов с возможностью применения скидок и налогов (через Admin Panel).

---

## Возможности

- Модель Item — товар с названием, описанием и ценой
- API для получения Stripe Session ID и перенаправления на форму оплаты
- Максимально простой HTML-страницы для отображения информации о товаре и заказе
- Модель Order — объединение нескольких товаров
- Модели Discount и Tax, применимые к заказу (через Админ Панель)
- Отображение моделей в Django Admin
- Работа с сессиями для хранения текущего заказа

---

## Страницы

| URL                          | Назначение                                        |
|------------------------------|---------------------------------------------------|
| `/admin/`                    | Админ Панель                                      |
| `/item/<id>/`                | Просмотр товара и кнопка покупки                  |
| `/buy/<id>/`                 | Получение Stripe Session ID для оплаты товара     |
| `/order/add/<item_id>/`      | Добавить товар в заказ                            |
| `/order/remove/<item_id>/`   | Удалить товар из заказа                           |
| `/order/clear/`              | Очистить заказ                                    |
| `/order/create/`             | Создает пустой заказ если его нет                 |
| `/order/current/`            | Просмотр текущего заказа                          |
| `/buy_order/<id>/`           | Покупка заказа через Stripe                       |

---

## Запуск

### 1. Клонируйте репозиторий

```
git clone https://github.com/AkihiroAck/OnlineStore_StripeAPI.git
cd OnlineStore_StripeAPI
```

### 2. Создайте и активируйте виртуальное окружение

Для Windows:

```
python -m venv venv
venv\Scripts\activate
```

Для macOS/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Установите зависимости

```
pip install -r requirements.txt
```

### 4. Настройте переменные окружения

Создайте .env файл в корне проекта (если используется python-decouple или аналогичный инструмент), либо пропишите значения напрямую в settings.py:

```
DEBUG=True
ALLOWED_HOSTS=*
SECRET_KEY=django-insecure-ixj++m6xf@b1@giupuhe4$5+ll8rst@0r5!g34_j$efe#*6tz0
STRIPE_PUBLIC_KEY=pk_test_51Rt5mjRyknxvpudx0N4k5b3IBD3LZrVsYWaeCQGup1LHweErMRyvnkQznPh7YVwK1vMkJfEE0OpD7ququNk5EPGF00DlXGjOuy
STRIPE_SECRET_KEY=sk_test_51Rt5mjRyknxvpudxaweaqNjVV8oNTSWE1wPiYevnUysgsSNmlXtDG1I3QuB1LwcmTRSAggova6spvRQ6QwzzqXgj00A0locDl4
```

### 5. Выполните миграции

```
python manage.py makemigrations
python manage.py migrate
```

### 6. Создайте суперпользователя (для доступа в админку)

```
python manage.py createsuperuser
```

### 7. Запустите сервер

```
python manage.py runserver
```
