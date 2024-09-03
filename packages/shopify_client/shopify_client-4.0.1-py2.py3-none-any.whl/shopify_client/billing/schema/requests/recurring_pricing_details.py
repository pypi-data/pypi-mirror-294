import dataclasses

from shopify_client.billing.constants import SubscriptionInterval
from shopify_client.billing.schema.requests.discount import Discount
from shopify_client.billing.schema.requests.price import Price


@dataclasses.dataclass
class RecurringPricingDetails:
    interval: SubscriptionInterval
    price: Price
    discount: Discount
