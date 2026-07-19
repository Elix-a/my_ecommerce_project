import pytest

from src.classes import Category, Product


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
