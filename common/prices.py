from core.models import Advertisement

from kontorshund.settings import NUMBER_OF_ADS_OFFERED_AT_DISCOUNT, REGULAR_PRICE, REGULAR_PRICE_STRING, PRICE_DURING_DISCOUNT, PRICE_DURING_DISCOUNT_STRING

count_of_ads_with_initial_payment = Advertisement.count_of_ads_with_intiial_payment()

CURRENT_PRICE = 0
CURRENT_PRICE_STRING = ''

if count_of_ads_with_initial_payment > NUMBER_OF_ADS_OFFERED_AT_DISCOUNT:
    CURRENT_PRICE = REGULAR_PRICE
    CURRENT_PRICE_STRING = REGULAR_PRICE_STRING
else:
    CURRENT_PRICE = PRICE_DURING_DISCOUNT
    CURRENT_PRICE_STRING = PRICE_DURING_DISCOUNT_STRING