from core.models import Advertisement

from kontorshund.settings import REGULAR_PRICE, REGULAR_PRICE_STRING, PRICE_DURING_DISCOUNT, PRICE_DURING_DISCOUNT_STRING


def get_number_of_ads_left_on_discounted_price():
    from kontorshund.settings import NUMBER_OF_ADS_OFFERED_AT_DISCOUNT
    count_of_ads_with_initial_payment = Advertisement.count_of_ads_with_intiial_payment()
    return NUMBER_OF_ADS_OFFERED_AT_DISCOUNT - count_of_ads_with_initial_payment

def get_current_ad_price_as_int_and_string():
    from kontorshund.settings import (
        NUMBER_OF_ADS_OFFERED_AT_DISCOUNT, 
        REGULAR_PRICE, 
        REGULAR_PRICE_STRING, 
        PRICE_DURING_DISCOUNT, 
        PRICE_DURING_DISCOUNT_STRING
    )

    count_of_ads_with_initial_payment = Advertisement.count_of_ads_with_intiial_payment()

    if count_of_ads_with_initial_payment > NUMBER_OF_ADS_OFFERED_AT_DISCOUNT:
        CURRENT_PRICE = REGULAR_PRICE
        CURRENT_PRICE_STRING = REGULAR_PRICE_STRING
    else:
        CURRENT_PRICE = PRICE_DURING_DISCOUNT
        CURRENT_PRICE_STRING = PRICE_DURING_DISCOUNT_STRING

    return CURRENT_PRICE, CURRENT_PRICE_STRING