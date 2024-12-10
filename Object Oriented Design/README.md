# Object-Oriented Design Patterns in Python

## Introduction

Design patterns are proven solutions to common programming problems. They help us write more maintainable, flexible, and reusable code. Let's explore the most important patterns, implemented in Python, with practical examples.

## Creational Patterns

Creational patterns deal with object creation mechanisms, trying to create objects in a manner suitable to the situation.

### 1. Singleton Pattern

The Singleton pattern ensures a class has only one instance and provides a global point of access to it. This is useful for managing shared resources like configuration settings or database connections.

```python
class DatabaseConnection:
    """
    A thread-safe singleton pattern implementation for database connections.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # Check if instance exists without acquiring lock first (performance)
        if cls._instance is None:
            with cls._lock:  # Thread safety
                # Double-check inside lock
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    # Initialize your database connection here
                    cls._instance.connection = None
        return cls._instance

    def connect(self):
        """Establish database connection if not already connected."""
        if self.connection is None:
            self.connection = create_db_connection()
        return self.connection

    def query(self, sql):
        """Execute SQL query using the singleton connection."""
        if self.connection is None:
            self.connect()
        return self.connection.execute(sql)

# Usage
db = DatabaseConnection()  # First instance
another_db = DatabaseConnection()  # Same instance
assert db is another_db  # True
```

### 2. Factory Pattern

The Factory pattern provides an interface for creating objects but lets subclasses decide which classes to instantiate.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    """Abstract base class for animals."""
    @abstractmethod
    def speak(self):
        pass

    @abstractmethod
    def move(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

    def move(self):
        return "Running on four legs"

class Bird(Animal):
    def speak(self):
        return "Chirp!"

    def move(self):
        return "Flying"

class AnimalFactory:
    """Factory class for creating different types of animals."""
    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        """
        Create an animal of the specified type.

        Args:
            animal_type: String indicating the type of animal to create

        Returns:
            An instance of the specified animal type

        Raises:
            ValueError: If animal_type is not recognized
        """
        if animal_type.lower() == "dog":
            return Dog()
        elif animal_type.lower() == "bird":
            return Bird()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

# Usage
factory = AnimalFactory()
dog = factory.create_animal("dog")
bird = factory.create_animal("bird")

print(dog.speak())  # "Woof!"
print(bird.move())  # "Flying"
```

### 3. Builder Pattern

The Builder pattern separates the construction of a complex object from its representation, allowing the same construction process to create different representations.

```python
class Computer:
    """Represents a computer with various components."""
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
        self.gpu = None

    def __str__(self):
        return f"Computer [CPU: {self.cpu}, Memory: {self.memory}GB, " \
               f"Storage: {self.storage}GB, GPU: {self.gpu}]"

class ComputerBuilder:
    """Builder class for constructing computers with different specifications."""
    def __init__(self):
        self.computer = Computer()

    def add_cpu(self, cpu: str) -> 'ComputerBuilder':
        """Add CPU to the computer."""
        self.computer.cpu = cpu
        return self  # Enable method chaining

    def add_memory(self, memory: int) -> 'ComputerBuilder':
        """Add RAM to the computer in GB."""
        self.computer.memory = memory
        return self

    def add_storage(self, storage: int) -> 'ComputerBuilder':
        """Add storage to the computer in GB."""
        self.computer.storage = storage
        return self

    def add_gpu(self, gpu: str) -> 'ComputerBuilder':
        """Add GPU to the computer."""
        self.computer.gpu = gpu
        return self

    def build(self) -> Computer:
        """Return the constructed computer."""
        return self.computer

class ComputerDirector:
    """Director class that defines common ways to build computers."""
    @staticmethod
    def build_gaming_computer(builder: ComputerBuilder) -> Computer:
        """Build a computer optimized for gaming."""
        return builder.add_cpu("Intel i9") \
                     .add_memory(32) \
                     .add_storage(2000) \
                     .add_gpu("RTX 3080") \
                     .build()

    @staticmethod
    def build_office_computer(builder: ComputerBuilder) -> Computer:
        """Build a computer suitable for office work."""
        return builder.add_cpu("Intel i5") \
                     .add_memory(16) \
                     .add_storage(500) \
                     .add_gpu("Integrated") \
                     .build()

# Usage
builder = ComputerBuilder()
director = ComputerDirector()

gaming_pc = director.build_gaming_computer(builder)
print(gaming_pc)  # Computer [CPU: Intel i9, Memory: 32GB, Storage: 2000GB, GPU: RTX 3080]

office_pc = director.build_office_computer(ComputerBuilder())
print(office_pc)  # Computer [CPU: Intel i5, Memory: 16GB, Storage: 500GB, GPU: Integrated]

# Custom build using method chaining
custom_pc = ComputerBuilder() \
    .add_cpu("AMD Ryzen 7") \
    .add_memory(64) \
    .add_storage(1000) \
    .add_gpu("RX 6800") \
    .build()
```

## Structural Patterns

Structural patterns deal with object composition and typically identify simple ways to realize relationships between different objects.

### 1. Adapter Pattern

The Adapter pattern allows incompatible interfaces to work together by wrapping an object in an adapter to make it compatible with another class.

```python
from abc import ABC, abstractmethod

class ModernPaymentGateway:
    """Modern payment processing system."""
    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount:.2f} through modern payment gateway")
        return True

class LegacyPaymentSystem:
    """Old payment system with different interface."""
    def old_payment(self, amount: float) -> str:
        print(f"Processing ${amount:.2f} through legacy system")
        return "SUCCESS"

class PaymentProcessor(ABC):
    """Abstract payment processor interface."""
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

class LegacyPaymentAdapter(PaymentProcessor):
    """Adapter to make legacy payment system compatible with modern interface."""
    def __init__(self, legacy_system: LegacyPaymentSystem):
        self.legacy_system = legacy_system

    def pay(self, amount: float) -> bool:
        # Adapt the legacy response to the modern boolean return type
        result = self.legacy_system.old_payment(amount)
        return result == "SUCCESS"

class PaymentService:
    """Payment service that works with PaymentProcessor interface."""
    def __init__(self, payment_processor: PaymentProcessor):
        self.payment_processor = payment_processor

    def process_payment(self, amount: float) -> bool:
        return self.payment_processor.pay(amount)

# Usage
# Modern payment system
modern_gateway = ModernPaymentGateway()
modern_service = PaymentService(modern_gateway)
modern_service.process_payment(100.00)

# Legacy payment system with adapter
legacy_system = LegacyPaymentSystem()
legacy_adapter = LegacyPaymentAdapter(legacy_system)
legacy_service = PaymentService(legacy_adapter)
legacy_service.process_payment(100.00)
```

### 2. Decorator Pattern

The Decorator pattern allows behavior to be added to individual objects dynamically, providing a flexible alternative to subclassing.

```python
from abc import ABC, abstractmethod
from typing import Optional

class Coffee(ABC):
    """Abstract base class for coffee."""
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

class SimpleCoffee(Coffee):
    """Basic coffee implementation."""
    def cost(self) -> float:
        return 2.0

    def description(self) -> str:
        return "Simple coffee"

class CoffeeDecorator(Coffee):
    """Base decorator class for coffee additions."""
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()

class MilkDecorator(CoffeeDecorator):
    """Adds milk to coffee."""
    def cost(self) -> float:
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        return f"{self._coffee.description()}, with milk"

class SugarDecorator(CoffeeDecorator):
    """Adds sugar to coffee."""
    def cost(self) -> float:
        return self._coffee.cost() + 0.2

    def description(self) -> str:
        return f"{self._coffee.description()}, with sugar"

class WhippedCreamDecorator(CoffeeDecorator):
    """Adds whipped cream to coffee."""
    def cost(self) -> float:
        return self._coffee.cost() + 1.0

    def description(self) -> str:
        return f"{self._coffee.description()}, with whipped cream"

# Usage
coffee = SimpleCoffee()
print(f"{coffee.description()}: ${coffee.cost():.2f}")

# Add milk
coffee_with_milk = MilkDecorator(coffee)
print(f"{coffee_with_milk.description()}: ${coffee_with_milk.cost():.2f}")

# Add sugar to coffee with milk
coffee_with_milk_sugar = SugarDecorator(coffee_with_milk)
print(f"{coffee_with_milk_sugar.description()}: ${coffee_with_milk_sugar.cost():.2f}")

# Create a complex coffee with multiple decorators
fancy_coffee = WhippedCreamDecorator(
    MilkDecorator(
        SugarDecorator(
            SimpleCoffee()
        )
    )
)
print(f"{fancy_coffee.description()}: ${fancy_coffee.cost():.2f}")
```

[Previous sections remain the same...]

## Behavioral Patterns

Behavioral patterns are concerned with communication between objects, how objects interact and distribute responsibility.

### 1. Observer Pattern

The Observer pattern establishes a one-to-many relationship between objects, where when one object changes state, all its dependents are notified and updated automatically.

```python
from abc import ABC, abstractmethod
from typing import List

class Subject(ABC):
    """Abstract subject that observers can watch."""

    def __init__(self):
        """Initialize empty list of observers."""
        self._observers: List[Observer] = []
        self._state = None

    def attach(self, observer: 'Observer') -> None:
        """Add an observer to the notification list."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer') -> None:
        """Remove an observer from the notification list."""
        self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observers of state change."""
        for observer in self._observers:
            observer.update(self._state)

class WeatherStation(Subject):
    """Concrete subject providing weather updates."""

    @property
    def temperature(self) -> float:
        return self._state

    @temperature.setter
    def temperature(self, value: float) -> None:
        """Set temperature and notify observers."""
        self._state = value
        self.notify()

class Observer(ABC):
    """Abstract observer that receives updates."""

    @abstractmethod
    def update(self, temperature: float) -> None:
        """Receive update from subject."""
        pass

class TemperatureDisplay(Observer):
    """Displays the temperature."""

    def update(self, temperature: float) -> None:
        print(f"Temperature Display: {temperature:.1f}°C")

class TemperatureAlert(Observer):
    """Alerts when temperature exceeds threshold."""

    def __init__(self, threshold: float):
        self.threshold = threshold

    def update(self, temperature: float) -> None:
        if temperature > self.threshold:
            print(f"Alert! Temperature {temperature:.1f}°C exceeds {self.threshold}°C")

# Usage
weather_station = WeatherStation()

# Create observers
display = TemperatureDisplay()
alert = TemperatureAlert(threshold=25.0)

# Register observers
weather_station.attach(display)
weather_station.attach(alert)

# Update temperature - all observers will be notified
weather_station.temperature = 24.0  # Display updates, no alert
weather_station.temperature = 27.0  # Display updates and alert triggers
```

### 2. Strategy Pattern

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. It lets the algorithm vary independently from clients that use it.

```python
from abc import ABC, abstractmethod
from typing import List

class PaymentStrategy(ABC):
    """Abstract base class for payment strategies."""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Process payment with the given strategy."""
        pass

class CreditCardPayment(PaymentStrategy):
    """Credit card payment strategy."""

    def __init__(self, card_number: str, expiry: str, cvv: str):
        self.card_number = card_number
        self.expiry = expiry
        self.cvv = cvv

    def pay(self, amount: float) -> bool:
        # In real implementation, this would integrate with a payment gateway
        print(f"Processing credit card payment of ${amount:.2f}")
        print(f"Card number: {'*' * 12}{self.card_number[-4:]}")
        return True

class PayPalPayment(PaymentStrategy):
    """PayPal payment strategy."""

    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> bool:
        print(f"Processing PayPal payment of ${amount:.2f}")
        print(f"PayPal account: {self.email}")
        return True

class CryptoPayment(PaymentStrategy):
    """Cryptocurrency payment strategy."""

    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float) -> bool:
        print(f"Processing crypto payment of ${amount:.2f}")
        print(f"Wallet: {self.wallet_address[:6]}...{self.wallet_address[-4:]}")
        return True

class ShoppingCart:
    """Shopping cart that uses payment strategies."""

    def __init__(self):
        self.items: List[tuple] = []  # List of (item, price) tuples

    def add_item(self, item: str, price: float) -> None:
        """Add item to cart."""
        self.items.append((item, price))

    def total(self) -> float:
        """Calculate total price."""
        return sum(price for _, price in self.items)

    def checkout(self, payment_strategy: PaymentStrategy) -> bool:
        """Checkout using the specified payment strategy."""
        amount = self.total()
        if amount == 0:
            raise ValueError("Cart is empty")

        # Process payment using the provided strategy
        return payment_strategy.pay(amount)

# Usage
# Create shopping cart and add items
cart = ShoppingCart()
cart.add_item("Laptop", 999.99)
cart.add_item("Mouse", 29.99)

# Create different payment strategies
credit_card = CreditCardPayment("1234567890123456", "12/24", "123")
paypal = PayPalPayment("user@example.com")
crypto = CryptoPayment("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")

# Checkout with different payment methods
cart.checkout(credit_card)  # Use credit card
cart.checkout(paypal)      # Use PayPal
cart.checkout(crypto)      # Use cryptocurrency
```

### 3. Command Pattern

The Command pattern encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class Command(ABC):
    """Abstract base class for commands."""

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass

    @abstractmethod
    def undo(self) -> None:
        """Undo the command."""
        pass

class TextEditor:
    """Text editor that maintains document state."""

    def __init__(self):
        self.text = ""

    def insert_text(self, text: str) -> None:
        """Insert text at current position."""
        self.text += text

    def delete_text(self, length: int) -> None:
        """Delete specified number of characters from end."""
        self.text = self.text[:-length]

    def get_text(self) -> str:
        """Get current text."""
        return self.text

class InsertTextCommand(Command):
    """Command to insert text."""

    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text

    def execute(self) -> None:
        self.editor.insert_text(self.text)

    def undo(self) -> None:
        self.editor.delete_text(len(self.text))

class DeleteTextCommand(Command):
    """Command to delete text."""

    def __init__(self, editor: TextEditor, length: int):
        self.editor = editor
        self.length = length
        self.deleted_text: Optional[str] = None

    def execute(self) -> None:
        # Store deleted text for undo
        self.deleted_text = self.editor.get_text()[-self.length:]
        self.editor.delete_text(self.length)

    def undo(self) -> None:
        if self.deleted_text:
            self.editor.insert_text(self.deleted_text)

class TextEditorInvoker:
    """Invoker that maintains command history."""

    def __init__(self, editor: TextEditor):
        self.editor = editor
        self.command_history: List[Command] = []

    def execute_command(self, command: Command) -> None:
        """Execute command and add to history."""
        command.execute()
        self.command_history.append(command)

    def undo_last_command(self) -> None:
        """Undo the last command."""
        if self.command_history:
            command = self.command_history.pop()
            command.undo()

# Usage
# Create editor and invoker
editor = TextEditor()
invoker = TextEditorInvoker(editor)

# Execute commands
insert_hello = InsertTextCommand(editor, "Hello ")
insert_world = InsertTextCommand(editor, "World!")
delete_mark = DeleteTextCommand(editor, 1)  # Delete exclamation mark

invoker.execute_command(insert_hello)
print(editor.get_text())  # "Hello "

invoker.execute_command(insert_world)
print(editor.get_text())  # "Hello World!"

invoker.execute_command(delete_mark)
print(editor.get_text())  # "Hello World"

# Undo commands
invoker.undo_last_command()  # Undo delete
print(editor.get_text())  # "Hello World!"

invoker.undo_last_command()  # Undo second insert
print(editor.get_text())  # "Hello "
```
