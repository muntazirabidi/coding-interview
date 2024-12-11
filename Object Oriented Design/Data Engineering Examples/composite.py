'''
Use Case: Managing hierarchical data structures or aggregating data from multiple sources into a single entity.
'''

class DataComponent:
    def __init__(self, name):
        self.name = name

    def show_data(self):
        raise NotImplementedError

class DataLeaf(DataComponent):
    def show_data(self):
        return f"Leaf Data: {self.name}"

class DataComposite(DataComponent):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def show_data(self):
        result = f"Composite Data: {self.name}\n"
        for child in self.children:
            result += f"  {child.show_data()}\n"
        return result

# Usage in a quant firm
root = DataComposite("All Market Data")
equities = DataComposite("Equities")
equities.add(DataLeaf("Stocks"))
equities.add(DataLeaf("ETFs"))

forex = DataComposite("Forex")
forex.add(DataLeaf("EUR/USD"))
forex.add(DataLeaf("USD/JPY"))

root.add(equities)
root.add(forex)

print(root.show_data())  # This will print a hierarchical structure of the data