# src/classes.py

import json
from typing import List


class Product:
    """Класс для представления продукта."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        """Инициализация экземпляра Product."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для представления категории товаров."""

    name: str
    description: str
    products: List[Product]

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: List[Product],
    ) -> None:
        """Инициализирует категорию и обновляет счётчики."""
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загружает категории и продукты из JSON-файла.
    Ожидаемый формат: список словарей, каждый с ключами
    'name', 'description', 'products'.
    Возвращает список объектов Category.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = []
    for cat_data in data:
        products = [
            Product(
                name=prod["name"],
                description=prod["description"],
                price=float(prod["price"]),
                quantity=int(prod["quantity"]),
            )
            for prod in cat_data["products"]
        ]
        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            products=products,
        )
        categories.append(category)
    return categories
