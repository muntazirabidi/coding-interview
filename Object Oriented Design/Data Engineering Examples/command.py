'''
Use Case: Managing and executing operations on data, like batch processing or scheduled tasks, with the ability to undo actions or log them.
'''

class DataCommand:
    def __init__(self, action):
        self.action = action

    def execute(self):
        return self.action()

class ProcessDataCommand(DataCommand):
    def __init__(self, data):
        super().__init__(lambda: f"Processing {data}")

class UndoCommand(DataCommand):
    def __init__(self, last_action):
        super().__init__(lambda: f"Undo: {last_action}")

# Usage in a quant firm
commands = []
process_cmd = ProcessDataCommand("Market Data")
commands.append(process_cmd)
print(process_cmd.execute())  # Should print: Processing Market Data

undo_cmd = UndoCommand(process_cmd.execute())
commands.append(undo_cmd)
print(undo_cmd.execute())  # Should print: Undo: Processing Market Data