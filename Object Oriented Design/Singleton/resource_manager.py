class ResourceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._resource = None  # Placeholder for any resource
        return cls._instance

    def acquire_resource(self, resource):
        if self._resource is None:
            self._resource = resource
            return True
        return False

    def release_resource(self):
        if self._resource is not None:
            temp = self._resource
            self._resource = None
            return temp
        return None

# Usage
manager = ResourceManager()
if manager.acquire_resource("Printer"):
    print("Resource acquired")
else:
    print("Resource not available")

# Try to acquire again
manager2 = ResourceManager()
if not manager2.acquire_resource("Printer"):
    print("Printer is already in use")

# Release the resource
released_resource = manager.release_resource()
print(f"Resource released: {released_resource}")