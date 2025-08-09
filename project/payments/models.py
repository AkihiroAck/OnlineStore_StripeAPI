from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=30)
    percent_off = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.name} ({self.percent_off}%)"


class Tax(models.Model):
    name = models.CharField(max_length=30)
    percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(
        Discount, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    tax = models.ForeignKey(
        Tax, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    def add_item(self, item_id):
        item = Item.objects.get(id=item_id)
        self.items.add(item)
        return self

    def get_total_price(self):
        total = Decimal('0')
        for item in self.items.all():
            total += item.price  # Суммируем Decimal цены
        
        if self.discount:
            # Конвертируем процент скидки в Decimal перед расчетом
            discount_percent = Decimal(str(self.discount.percent_off)) / Decimal('100')
            total *= (Decimal('1') - discount_percent)
        
        if self.tax:
            tax_percent = Decimal(str(self.tax.percentage)) / Decimal('100')
            total *= (Decimal('1') + tax_percent)
        
        return total.quantize(Decimal('0.01'))  # Округляем до 2 знаков

    def __str__(self):
        return f"Order #{self.id}"
    