from .loader import loadnlp


class SpacyNLPMixin:
    model_name: str

    def _set_model_name(self, model_name):
        self.model_name = model_name

    def _get_language(self):
        return loadnlp(self.model_name)
