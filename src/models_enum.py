import enum

class ProductStatus(str, enum.Enum):
    new_product = 'new_product'
    modified_ai = 'modified_ai'
    not_modified_ai = 'not_modified_ai'

class MarketplaceType(str, enum.Enum):
    OZON = "ozon"
    WILDBERRIES = "wb"
    YANDEX = "yandex"

