from store.models import ProductModel
from typing import List


class Product:
    def __init__(self, model: ProductModel = None, sku: str = None):
        if sku is None and model is None:
            raise Exception('Product must get SKU or ProductModel to be created')
        elif model:
            self.model = model
        else:
            self.model = ProductModel.objects.get(sku=sku)
        self.price = self.model.price
        self.main_image = self.model.main_image
        self.title = self.model.title
        self.sku = self.model.sku
        self.is_digital = self.model.is_digital

    @classmethod
    def get_product_by_sku(cls, sku: str) -> 'Product':
        return Product(sku=sku)

    @classmethod
    def get_all(cls) -> List['Product']:
        return [Product(model=model) for model in ProductModel.objects.all()]
