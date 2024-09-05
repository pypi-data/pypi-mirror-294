import json
import base64
import sqlite3
from datetime import datetime

from src.aicacia.Document import Document, DocumentSection, MediaType
from src.aicacia.DocumentExporter import DocumentExporter
from src.aicacia.PreprocessingModel import PreprocessingModel


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Document):
            return obj.__dict__
        elif isinstance(obj, DocumentSection):
            return obj.__dict__
        elif isinstance(obj, MediaType):
            return obj.value
        elif isinstance(obj, bytes):
            return base64.b64encode(obj).decode('utf-8')
        else:
            return super().default(obj)


class FileDocumentExporter(DocumentExporter):
    def __init__(self, path, batch_size: int = 128, preprocessing_model: PreprocessingModel | None = None):
        super().__init__(batch_size, preprocessing_model)
        self.fo = open(path, "a+")
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS docs (id TEXT PRIMARY KEY, hash INTEGER, doi TEXT, data TEXT)'
        )

    def _flush(self, docs: list[Document]):
        for doc in docs:
            self.cur.execute(
                "INSERT INTO docs (id, hash, doi, data) VALUES (?, ?, ?, ?)",
                (doc.id, doc.content_hash, doc.doi, json.dumps(doc, cls=Encoder),)
            )

        self.con.commit()

    def close(self) -> None:
        self.con.close()
