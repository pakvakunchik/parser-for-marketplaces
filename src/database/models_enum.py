import enum

class ProductStatus(str, enum.Enum):
    new_product = 'new_product'
    modified_ai = 'modified_ai'
    not_modified_ai = 'not_modified_ai'



