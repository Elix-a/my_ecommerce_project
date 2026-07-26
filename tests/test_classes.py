# tests/test_classes.py

import json
from pathlib import Path

import pytest
from pytest import CaptureFixture

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
    expected_str = "Молоко, 89.9 руб. Остаток: 10 шт.\n"
    assert sample_category.products == expected_str


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


def test_add_product_increases_count() -> None:
    """Проверяет, что add_product увеличивает product_count."""
    initial_product_count = Category.product_count
    cat = Category("Тест", "Тестовая категория", [])
    product = Product("Товар", "Описание", 100, 1)
    cat.add_product(product)
    assert Category.product_count == initial_product_count + 1
    assert "Товар, 100 руб. Остаток: 1 шт." in cat.products


def test_add_product_appends_to_private_list() -> None:
    """Проверяет, что продукт добавляется и отображается в геттере."""
    cat = Category("Тест", "Описание", [])
    p1 = Product("A", "desc", 10, 2)
    p2 = Product("B", "desc", 20, 3)
    cat.add_product(p1)
    cat.add_product(p2)
    output = cat.products
    assert "A, 10 руб. Остаток: 2 шт." in output
    assert "B, 20 руб. Остаток: 3 шт." in output


def test_price_getter_and_setter() -> None:
    """Проверяет работу геттера и сеттера цены."""
    product = Product("Test", "desc", 100.0, 1)
    assert product.price == 100.0
    product.price = 150.0
    assert product.price == 150.0


def test_price_setter_negative(
    capsys: CaptureFixture[str],
) -> None:
    """Сеттер не должен менять цену на отрицательную."""
    product = Product("Test", "desc", 100.0, 1)
    product.price = -50.0
    assert product.price == 100.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_price_setter_zero(
    capsys: CaptureFixture[str],
) -> None:
    """Сеттер не должен менять цену на ноль."""
    product = Product("Test", "desc", 100.0, 1)
    product.price = 0.0
    assert product.price == 100.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_new_product_classmethod() -> None:
    """Проверяет создание продукта через класс-метод new_product."""
    data = {
        "name": "Телефон",
        "description": "Смартфон",
        "price": 30000,
        "quantity": 5,
    }
    product = Product.new_product(data)
    assert product.name == "Телефон"
    assert product.description == "Смартфон"
    assert product.price == 30000.0
    assert product.quantity == 5


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
    output = categories[0].products
    assert "Samsung Galaxy C23 Ultra" in output
    assert "Iphone 15" in output
