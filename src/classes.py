import json
from abc import ABC, abstractmethod
from typing import Any, List


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.
    Объявляет общую функциональность, обязательную для реализации.
    """

    @abstractmethod
    def calculate_total(self) -> float:
        """
        Рассчитывает полную стоимость товара на складе.
        Должен быть реализован в дочерних классах.
        """
        pass


class ProductMixin:
    """
    Миксин, который при создании объекта печатает в консоль информацию о том,
    от какого класса и с какими параметрами был создан объект.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        args_repr = [repr(arg) for arg in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_params = args_repr + kwargs_repr
        print(f"Создан объект {self.__class__.__name__}({', '.join(all_params)})")


class Product(BaseProduct, ProductMixin):
    """Класс для представления продукта."""

    name: str
    description: str
    __price: float
    quantity: int

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        """Инициализация экземпляра Product."""
        super().__init__(name, description, price, quantity)
        self.name = name
        self.description = description
        self.__price = price
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.quantity = quantity

    def calculate_total(self) -> float:
        """Возвращает полную стоимость товара на складе."""
        return self.price * self.quantity

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой на положительное значение."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = new_price

    @classmethod
    def new_product(cls, data: dict) -> "Product":
        """
        Класс-метод для создания продукта из словаря.
        Ожидаемые ключи: name, description, price, quantity.
        """
        return cls(
            name=data["name"],
            description=data["description"],
            price=float(data["price"]),
            quantity=int(data["quantity"]),
        )

    def __str__(self) -> str:
        """Строковое отображение продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Сложение двух продуктов одного класса."""
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса")
        return self.calculate_total() + other.calculate_total()


class Smartphone(Product):
    """Класс для представления смартфона."""

    efficiency: float
    model: str
    memory: int
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        """Инициализация экземпляра Smartphone."""
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для представления травы газонной."""

    country: str
    germination_period: str
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        """Инициализация экземпляра LawnGrass."""
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс для представления категории товаров."""

    name: str
    description: str
    __products: List[Product]

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: List[Product],
    ) -> None:
        """
        Инициализация категории.
        Список продуктов сохраняется в приватный атрибут.
        """
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт в приватный список товаров категории.
        Принимает только экземпляры Product или его наследников.
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты типа Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер, возвращающий строку с информацией о всех продуктах."""
        if not self.__products:
            return ""
        result = ""
        for prod in self.__products:
            result += f"{prod}\n"
        return result

    def __str__(self) -> str:
        """Строковое отображение категории."""
        total_quantity = sum(prod.quantity for prod in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def middle_price(self) -> float:
        """
        Рассчитывает среднюю цену товаров в категории.
        В случае пустой категории возвращает 0.
        """
        try:
            total_price = sum(prod.price for prod in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0.0


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
