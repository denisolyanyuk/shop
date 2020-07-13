from store.models import ProductModel


class Product:
    def __init__(self, model: ProductModel = None, sku: str = None):
        if sku is None and model is None:
            raise Exception('Product must get SKU or ProductModel to be created')
        elif model:
            self.model = model
        else:
            self.model = ProductModel.objects.get(SKU=sku)
        self.price = self.model.price
        self.main_image = self.model.main_image
        self.title = self.model.title
        self.SKU = self.model.SKU
        self.is_digital = self.model.is_digital


class ProductFactory:
    @staticmethod
    def get_product_by_sku(sku: str):
        return ProductModel.objects.get(SKU=sku)

    @staticmethod
    def get_all():
        return [Product(model=model) for model in ProductModel.objects.all()]