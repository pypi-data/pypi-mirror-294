import uuid
from abc import ABC, abstractmethod
from datetime import datetime

import tzlocal

from src.aicacia_document_exporter.Document import Document
from src.aicacia_document_exporter.PreprocessingModel import PreprocessingModel


def split_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


class DocumentExporter(ABC):
    def __init__(self, batch_size: int = 128, preprocessing_model: PreprocessingModel | None = None):
        self.batch = []
        self.max_batch_size = batch_size
        self.preprocessing_model = preprocessing_model

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if len(self.batch) > 0:
            self._preprocess_and_flush(self.batch)
            self.batch.clear()

        self.close()

    def insert(self, docs: list[Document]):
        self._check_docs_type(docs)
        self._fill_missing_data(docs)

        self.batch.extend(docs)

        batch_size = len(self.batch)

        if batch_size == self.max_batch_size:
            self._preprocess_and_flush(self.batch)
            self.batch.clear()
        elif batch_size > self.max_batch_size:
            for chunk in split_list(self.batch, self.max_batch_size):
                self._preprocess_and_flush(chunk)
            self.batch.clear()

    def _preprocess_and_flush(self, docs: list[Document]):
        if self.preprocessing_model is not None:
            self.preprocessing_model.preprocess_batch(docs)

        self._flush(docs)

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def _flush(self, docs: list[Document]):
        pass

    @staticmethod
    def _check_docs_type(docs: list[Document]):
        for doc in docs:
            if not isinstance(doc, Document):
                raise TypeError(f"Expected argument of type 'Document', but got {type(doc).__name__}")

    @staticmethod
    def _fill_missing_data(docs: list[Document]):
        for doc in docs:
            if doc.id is None:
                doc.id = str(uuid.uuid4())

            if doc.sourced_date is None:
                doc.sourced_date = datetime.now(tzlocal.get_localzone())
            elif doc.sourced_date.tzinfo is None:
                doc.sourced_date = doc.sourced_date.replace(tzinfo=tzlocal.get_localzone())

            if doc.revision_date is None:
                doc.revision_date = doc.sourced_date