import json
from typing import List


class Product:
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
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

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
        return self.price * self.quantity + other.price * other.quantity


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
    germination_period: int
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
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
