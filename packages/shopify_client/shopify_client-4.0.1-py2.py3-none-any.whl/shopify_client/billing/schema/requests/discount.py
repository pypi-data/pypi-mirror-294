import dataclasses

from typing import Optional
from shopify_client.billing.schema.requests.discount_value import DiscountValue


@dataclasses.dataclass
class Discount:
    value: DiscountValue
