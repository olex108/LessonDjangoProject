"""
Scripts for Django shell
"""

# import
from catalog.models import Category, Product

# Create
category_1 = Category.objects.create(
    name="Смартфоны", description="Смартфон это телефон, имеющий начинку и функционал почти как у компьютера"
)
category_2 = Category.objects.create(
    name="Смарт-часы", description="Типовыми функциями смарт-часов и браслетов являются подсчет количества шагов"
)

Product_1 = Product.objects.create(
    name="Samsung Galaxy S25 Ultra",
    description="Samsung Galaxy S25 Ultra - новый взгляд на будущее мобильных технологий",
    price=99990,
    category=category_1,
)

Product_2 = Product.objects.create(
    name="Samsung Galaxy A56",
    description="Samsung Galaxy A56 – это новый смартфон 2025 года с мощным процессором Exynos 1580",
    price=27390,
    category=category_1,
)

Product_3 = Product.objects.create(
    name="Samsung Galaxy Watch8",
    description="Смарт-часы Samsung Galaxy Watch 8 44mm — это именно то, что вам нужно!",
    price=20990,
    category=category_2,
)

Product_4 = Product.objects.create(
    name="Samsung Galaxy Watch8 Classic",
    description="Умные часы Samsung Galaxy Watch8 Classic 46mm — это не просто аксессуар, а мощный инструмент",
    price=25990,
    category=category_2,
)

categories = Category.objects.all()
for category in categories:
    print(category.id, category.name, category.description)

products = Product.objects.all()
for product in products:
    print(product.id, product.name, product.description, product.price)

# Get list of products filtered by category
products_smartphones = Product.objects.filter(category=category_1)
for product in products_smartphones:
    print(product.id, product.name, product.description, product.price)

# Change price for product
product_change = Product.object.get(name="Samsung Galaxy S25 Ultra")
product_change.price = 90000
product_change.save()

# Delete product
product_del = Product.object.get(name="Samsung Galaxy S25 Ultra")
product_del.delete()
