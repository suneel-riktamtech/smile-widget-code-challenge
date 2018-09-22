from django.db import models
import datetime
from datetime import date

class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')
    
    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)
    
    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)

class ProductPrice(models.Model):
    black_fridays = [23, 24, 25]
    black_friday_prices = [80000, 0]
    new_year = date(2019, 1, 1)
    new_year_prices = [120000, 12500]
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)	
    def getPrice(self, date_submitted):
        if not isinstance(date_submitted, date):
            raise TypeError('Please enter Valid Date')
        if date_submitted.month == 11 and date_submitted.day in self.black_fridays:
            if self.product.code == 'big_widget':
                return self.black_friday_prices[0]
            else:
                return self.black_friday_prices[1]
        elif self.new_year <= date_submitted:
            if self.product.code == 'big_widget':
                return self.new_year_prices[0]
            else:
                return self.new_year_prices[1]
        else:
            return self.product.price
    def __str__(self):
        return "{} - {}".format(self.product.name, self.product.code)        