class ModelManager:
    def __init__(self):
        self.models = {}

    def add_model(self, model_type, model_instance):
        self.models[model_type] = model_instance

    def get_model(self, model_type):
        return self.models.get(model_type)
    