from abc import ABC, abstractmethod

from src.aicacia.Document import Document


class PreprocessingModel(ABC):
    @abstractmethod
    def preprocess_batch(self, docs: list[Document]):
        pass
