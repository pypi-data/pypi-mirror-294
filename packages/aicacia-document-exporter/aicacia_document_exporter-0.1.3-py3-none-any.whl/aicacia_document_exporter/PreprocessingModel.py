from abc import ABC, abstractmethod

from src.aicacia_document_exporter.Document import Document


class PreprocessingModel(ABC):
    @abstractmethod
    def preprocess_batch(self, docs: list[Document]):
        pass
