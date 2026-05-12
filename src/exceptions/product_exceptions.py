class ProductNotFoundError(Exception):
    def __init__(self, barcode):
        self.barcode = barcode
        super().__init__(f"Товар с кодом {barcode} не найден у поставщика")