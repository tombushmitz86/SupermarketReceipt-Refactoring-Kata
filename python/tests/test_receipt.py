from model_objects import Discount, Product
from receipt import Receipt

def test_total_price():
    receipt = Receipt()
    receipt.add_product(Product('xbox', 100), 2, 100, 200)
    receipt.add_discount(Discount(Product('apples', 2), "foobar", -50))
    assert receipt.total_price() == 150


def test_total_price_should_be_zero_if_no_items():
    receipt = Receipt()
    assert receipt.total_price() == 0

# def test_total_price_should_ceil_zero_if_negative():
#     receipt = Receipt()
#     receipt.add_discount(Discount(Product('apples', 2), "foobar", -50))
#     assert receipt.total_price() == 0

