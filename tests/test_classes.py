# tests/test_classes.py

import json
from pathlib import Path

import pytest

from src.classes import Category, Product, load_categories_from_json


@pytest.fixture
def sample_product() -> Product:
    return Product(
        name="Молоко",
        description="Свежее молоко 3.2%",
        price=89.90,
        quantity=10,
    )


@pytest.fixture
def sample_category(sample_product: Product) -> Category:
    return Category(
        name="Продукты",
        description="Категория продуктов питания",
        products=[sample_product],
    )


def test_product_initialization(sample_product: Product) -> None:
    """Проверяет корректность инициализации продукта."""
    assert sample_product.name == "Молоко"
    assert sample_product.description == "Свежее молоко 3.2%"
    assert sample_product.price == 89.90
    assert sample_product.quantity == 10


def test_category_initialization(
    sample_category: Category,
    sample_product: Product,
) -> None:
    """Проверяет корректность инициализации категории."""
    assert sample_category.name == "Продукты"
    assert sample_category.description == "Категория продуктов питания"
    assert len(sample_category.products) == 1
    assert sample_category.products[0] == sample_product


def test_category_count_increment() -> None:
    """Проверяет увеличение счётчика категорий."""
    initial_count = Category.category_count
    product = Product("Хлеб", "Ржаной", 50.0, 20)
    Category("Выпечка", "Хлебобулочные изделия", [product])
    assert Category.category_count == initial_count + 1


def test_product_count_increment() -> None:
    """Проверяет увеличение счётчика товаров."""
    initial_product_count = Category.product_count
    products = [
        Product("Чай", "Зелёный", 120.0, 5),
        Product("Кофе", "Арабика", 250.0, 3),
    ]
    Category("Напитки", "Чай и кофе", products)
    assert Category.product_count == initial_product_count + len(products)


def test_load_categories_from_json(tmp_path: Path) -> None:
    """Проверяет загрузку категорий из JSON-файла."""
    test_data = [
        {
            "name": "Смартфоны",
            "description": "Смартфоны...",
            "products": [
                {
                    "name": "Samsung Galaxy C23 Ultra",
                    "description": "256GB, Серый цвет, 200MP камера",
                    "price": 180000.0,
                    "quantity": 5,
                },
                {
                    "name": "Iphone 15",
                    "description": "512GB, Gray space",
                    "price": 210000.0,
                    "quantity": 8,
                },
            ],
        }
    ]
    file_path = tmp_path / "test_products.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False)

    categories = load_categories_from_json(str(file_path))
    assert len(categories) == 1
    assert categories[0].name == "Смартфоны"
    assert len(categories[0].products) == 2
    assert categories[0].products[0].name == "Samsung Galaxy C23 Ultra"
    assert categories[0].products[0].price == 180000.0
    assert categories[0].products[1].quantity == 8
