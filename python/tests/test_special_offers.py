import pytest

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from receipt_printer import ReceiptPrinter


@pytest.fixture
def catalog():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 2.00)
    return catalog

@pytest.fixture
def cart():
    cart = ShoppingCart()
    return cart

@pytest.fixture
def teller(catalog):
    teller = Teller(catalog)
    return teller

@pytest.fixture
def toothbrush_product(catalog):
    return Product("toothbrush", ProductUnit.EACH)

@pytest.fixture
def toothpaste_product(catalog):
    return Product("toothpaste", ProductUnit.EACH)

def test_handle_offers_only_within_options(cart, teller, toothbrush_product):
    cart.add_item_quantity(toothbrush_product, 2)
    receipt = teller.checks_out_articles_from(cart)
    teller.add_special_offer('just an offer', toothbrush_product, 1.5)
    receipt = teller.checks_out_articles_from(cart)
    assert len(receipt.discounts) == 0

def test_handle_offers_only_for_available_products(cart, teller, toothbrush_product):
    apples = Product("apples", ProductUnit.KILO)
    cart.add_item_quantity(toothbrush_product, 2)
    receipt = teller.checks_out_articles_from(cart)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, apples, 1.5)
    receipt = teller.checks_out_articles_from(cart)
    assert len(receipt.discounts) == 0

def test_three_for_two_offer(cart, teller, toothbrush_product):
    cart.add_item_quantity(toothbrush_product, 2)
    receipt = teller.checks_out_articles_from(cart)
    # No discount since we took only 2 items
    assert len(receipt.discounts) == 0
    cart.add_item_quantity(toothbrush_product, 1)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush_product, 1.5)
    receipt = teller.checks_out_articles_from(cart)
    offer_discount = receipt.discounts[0]
    assert offer_discount.product == toothbrush_product
    assert offer_discount.description == f'3 for 2'
    assert offer_discount.discount_amount == -2
    # after discount on 6 tubes = 4
    assert 4.0 == pytest.approx(receipt.total_price(), 0.01)


def test_ten_percent_offer(cart, teller, toothbrush_product):
    cart.add_item_quantity(toothbrush_product, 2)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush_product, 10.0)
    receipt = teller.checks_out_articles_from(cart)
    assert len(receipt.discounts) == 1
    offer_discount = receipt.discounts[0]
    assert offer_discount.product == toothbrush_product
    assert offer_discount.description == f'10.0% off'
    assert offer_discount.discount_amount == -0.4
    assert 3.6 == pytest.approx(receipt.total_price(), 0.01)



def test_two_for_amount_offer(cart, teller, toothbrush_product):
    cart.add_item_quantity(toothbrush_product, 6)
    # Normal cost is 6 * 2.0  = 12
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush_product, 1.5)
    receipt = teller.checks_out_articles_from(cart)
    assert len(receipt.discounts) == 1
    offer_discount = receipt.discounts[0]
    assert offer_discount.product == toothbrush_product
    assert offer_discount.description == f'2 for 1.5'
    assert offer_discount.discount_amount == -7.5
    # after discount on 6 tubes = 4.5
    assert 4.5 == pytest.approx(receipt.total_price(), 0.01)


def test_five_for_amount_offer(cart, teller, toothbrush_product):
    cart.add_item_quantity(toothbrush_product, 6)
    # Normal cost is 6 * 2.0  = 12
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush_product, 8.0)
    receipt = teller.checks_out_articles_from(cart)
    assert len(receipt.discounts) == 1
    offer_discount = receipt.discounts[0]
    assert offer_discount.product == toothbrush_product
    assert offer_discount.description == f'5 for 8.0'
    assert offer_discount.discount_amount == -2.0
    # after discount on 6 tubes = 10
    assert 10 == pytest.approx(receipt.total_price(), 0.01)


def test_no_double_offers_so_only_latest_offer_counts(cart, teller, toothbrush_product):
    cart.add_item_quantity(toothbrush_product, 3)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush_product, 1.5)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush_product, 10.0)
    
    receipt = teller.checks_out_articles_from(cart)
    assert len(receipt.discounts) == 1
    offer_discount = receipt.discounts[0]
    assert offer_discount.description == f'10.0% off'