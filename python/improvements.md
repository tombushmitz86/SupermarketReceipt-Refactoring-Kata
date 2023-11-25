
## improvements

  
  
  

    Teller.add_item_quantity

 no error handling or input validation (0 items)

`ShoppingCart.handle_offers` "x" variable naming is not by any naming convention and should be something more explicit like "offer_base_count"

`Receipt.total_price` does not round to zero if the discounts are larger than the sale price (can be negative)

`ReceiptPrinter`: white space size is needed to be calculated as the minimum of a the largest on include at least one whitespace (product string + its size) for readability (to avoid cases like e.g toothbrush9)

`Product.quantity` seems to be a bit unnecessary, since every method that adds a Product (Catalog and Receipt) also receives an argument of quantity

### General Improvements

1. **no logging or audit**
there is a need to add audit trail or log across the project to see events like discount being added or removed, code redeem, admin cashier activities etc. 


2. instead of calculating price and discount in two phases we can iterate over items and calculate their discount and final price on one iteration

3. Although double discounts is not common we can have the option to allow them and extending Teller.add_special_offer to have multiple offers with priorities (like 3 for 2 and upon that 10 percent discount)

4. I would add voucher ability like REDEEM CODE, and there are two places which this can be implemented on:

	1) as an offer: `SpecialOffer.CODE_REDEEM` and add it as argument: `teller.add_special_offer(SpecialOfferType.CODE_REDEEM, None, 150)`

	this require the modification of add_special_offer to accept None as product to indicate this is a general special offer and also modify ShoppingCart.handle_offers to perform iteration also on offers that are not product-bound

	benefit: we have the code redeem as a discount item in the receipt for audit trail (printing)

	2) adding to `Receipt.add_redeem_code(amount: int)` so it will modify the total_amount

	benefit: minimal changes

  
  
  5. ShoppingCart:

* no item reset (we added apples but removed 5 of them and what to re-add them)

* no cart reset (e.g wrong offers that have been handled and need to be reset)

6. ReceiptPrinter

* add interfaces with different types of prints and formats (email, html templates, raw text etc..)

7. lack of type hinting across the project


### In general the discount mechanism is somewhere cumbersome and hard to understand, I might put in implementation where

instead of discount I would just calculate the amount due to pay and subtract that from the normal price, e.g

we have 2 tvs for 1000, instead of calculating the discount by buying 3 tvs I would calculate the 1000 on two tvs + normal price of a single

item and then subtract the regular of 3 tvs from the (2 tvs for 1000)

  

### Improvements that have been made as part of the assignment
* 1. OfferType has been generalize into fewer options that include the rest such as 

	    SpecialOfferType.X_PERCENT_DISCOUNT ( the ability to create different discounts 15,25,50 without creating new types making it more seamless)

	    SpecialOfferType.X_FOR_AMOUNT
			and the offer handling the produces `Discount` has been moved to the model itself to a class method

	note :
	* tests have been adjusted to accompany this change
	* SpecialOfferType.THREE_FOR_TWO can also be part of `SpecialOfferType.X_FOR_AMOUNT` since AMOUNT can be the price of `TWO` hence making it one type of `SpecialOfferType.X_FOR_AMOUNT_OF_Y` and just passing two arguments of X,Y
	due to lack of time I did not implement this.
* 2.  ReceiptPrinter have been "boilerplate-ed" to have different types of printing (html, sms, raw print), test have been adjusted
