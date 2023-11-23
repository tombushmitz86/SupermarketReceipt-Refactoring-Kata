from enum import Enum
import math
from typing import Optional


class Product:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit


class ProductQuantity:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4
    X_FOR_AMOUNT = 5
    X_PERCENT_DISCOUNT = 6


class Discount:
    def __init__(self, product, description, discount_amount):
        self.product = product
        self.description = description
        self.discount_amount = discount_amount


class Offer:
    def __init__(self, offer_type, product, argument, quantity_on_offer: int = None):
        self.offer_type = offer_type
        self.product = product
        self.argument = argument
        self.quantity_on_offer = quantity_on_offer
        

    def produce_discount(self, quantity: int, unit_price: int, p: Product) -> Optional[Discount]:
        quantity_as_int = int(quantity) 
        if self.offer_type == SpecialOfferType.X_FOR_AMOUNT:
            number_of_items_floored = math.floor(quantity_as_int / self.quantity_on_offer)
            if quantity_as_int >= self.quantity_on_offer:
                total = self.argument * (number_of_items_floored) + quantity_as_int % self.quantity_on_offer * unit_price
                discount_n = unit_price * quantity - total
                verbose_string = f'{self.quantity_on_offer} for {str(self.argument)}'
                return Discount(p, verbose_string, -discount_n)
        
        elif self.offer_type == SpecialOfferType.X_PERCENT_DISCOUNT:
            verbose_string = f'{self.argument}% off'
            return Discount(p, verbose_string, -quantity * unit_price * self.argument / 100.0)
        
        elif self.offer_type == SpecialOfferType.THREE_FOR_TWO:
            number_of_x = math.floor(quantity_as_int / 3)
            if self.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                discount_amount = quantity * unit_price - (
                            (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price)
                verbose_string = "3 for 2"
                return Discount(p, verbose_string, -discount_amount)

