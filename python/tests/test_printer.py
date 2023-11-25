import pytest
from model_objects import Discount, Product
from receipt import Receipt
from receipt_printer import ReceiptPrinterStandard

@pytest.fixture
def receipt_with_items():
    receipt = Receipt()
    p = Product('toothbrush', 2)
    receipt.add_product(p, 2, 2.0, 4)
    return receipt

@pytest.fixture
def receipt_with_discounted_item():
    receipt = Receipt()
    p = Product('toothbrush', 2)
    receipt.add_product(p, 2, 2.0, 4)
    receipt.add_discount(Discount(p, 'a discount', -2))
    return receipt

@pytest.fixture
def receipt_printer():
    return ReceiptPrinterStandard(columns=20)

@pytest.fixture
def standard_output():
    return "toothbrush      4.00\n  2.00 * 2.000\n\nTotal:          4.00\n"

@pytest.fixture
def standard_output_with_discount():
    return "toothbrush      4.00\n  2.00 * 2.000\na discount (toothbrush)-2.00\n\nTotal:          2.00\n"

class TestStandardPrinter:
    def test_receipt_printer_regular(self, receipt_printer, receipt_with_items, standard_output):
        assert receipt_printer.print_receipt(receipt_with_items) == standard_output

    def test_receipt_printer_with_discount(self, receipt_printer, receipt_with_discounted_item, standard_output_with_discount):
        assert receipt_printer.print_receipt(receipt_with_discounted_item) == standard_output_with_discount


######## This is a standard printing of receipt
# if the ReceiptPrinterAbstract is extended to something like ReceiptPrinterHTML or ReceiptPrinterSMS
# we can have more TestXXXPrinter classes 
# and use fixture that on test setup can load html or sms output to assert on e.g



# @pytest.fixture
# def standard_html():
#     pass

# @pytest.fixture
# def html_with_discount():
#     pass

# class TestHTMLPrinter:
#     def test_receipt_printer_regular(self, receipt_printer, receipt_with_items, standard_html):
#         assert receipt_printer.print_receipt(receipt_with_items) == standard_output

#     def test_receipt_printer_with_discount(self, receipt_printer, receipt_with_discounted_item, html_with_discount):
#         assert receipt_printer.print_receipt(receipt_with_discounted_item) == standard_output_with_discount











