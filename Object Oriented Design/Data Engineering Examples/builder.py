'''
Use Case: Building complex data models or configurations for data pipelines with step-by-step construction.

'''

class DataPipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def run(self):
        print(f"Running pipeline with steps: {', '.join(self.steps)}")

class PipelineBuilder:
    def __init__(self):
        self.pipeline = DataPipeline()

    def add_data_fetch(self):
        self.pipeline.add_step("Fetch Data")
        return self

    def add_data_clean(self):
        self.pipeline.add_step("Clean Data")
        return self

    def add_data_transform(self):
        self.pipeline.add_step("Transform Data")
        return self

    def get_pipeline(self):
        return self.pipeline

# Usage in a quant firm
builder = PipelineBuilder()
pipeline = builder.add_data_fetch().add_data_clean().add_data_transform().get_pipeline()
pipeline.run()  # Should print: Running pipeline with steps: Fetch Data, Clean Data, Transform Data