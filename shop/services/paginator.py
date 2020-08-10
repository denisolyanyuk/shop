from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ShopPaginator(Paginator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def page(self, number):
        try:
            objects = super(ShopPaginator, self).page(number)
        except PageNotAnInteger:
            # Если страница не является целым числом, возвращаем первую страницу.
            objects = super(ShopPaginator, self).page(1)
        except EmptyPage:
            # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
            objects = super(ShopPaginator, self).page(self.num_pages)

        return objects
