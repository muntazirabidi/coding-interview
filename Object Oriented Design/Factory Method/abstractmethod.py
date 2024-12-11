from abc import ABC, abstractmethod

class AbstractClassExample(ABC):
    @abstractmethod
    def do_something(self):
        """This method must be implemented by subclasses."""
        pass

    def do_something_else(self):
        """This method can be used as-is or overridden by subclasses."""
        print("Doing something else")

# Attempting to instantiate the abstract class directly will raise an error
# abstract_instance = AbstractClassExample()  # TypeError: Can't instantiate abstract class AbstractClassExample with abstract method do_something

class ConcreteClass(AbstractClassExample):
    def do_something(self):
        """Implementation of the abstract method."""
        print("Doing something specific")

# This is correct because ConcreteClass implements all abstract methods
concrete_instance = ConcreteClass()
concrete_instance.do_something()  # Prints: Doing something specific
concrete_instance.do_something_else()  # Prints: Doing something else