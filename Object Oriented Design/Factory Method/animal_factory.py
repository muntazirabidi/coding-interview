from abc import ABC, abstractmethod

# Abstract Product
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

# Concrete Products
class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

# Creator
class AnimalFactory(ABC):
    @abstractmethod
    def create_animal(self):
        pass

# Concrete Creators
class DogFactory(AnimalFactory):
    def create_animal(self):
        return Dog()

class CatFactory(AnimalFactory):
    def create_animal(self):
        return Cat()

# Usage
dog_factory = DogFactory()
cat_factory = CatFactory()

dog = dog_factory.create_animal()
cat = cat_factory.create_animal()

print(dog.speak())  # Outputs: Woof!
print(cat.speak())  # Outputs: Meow!