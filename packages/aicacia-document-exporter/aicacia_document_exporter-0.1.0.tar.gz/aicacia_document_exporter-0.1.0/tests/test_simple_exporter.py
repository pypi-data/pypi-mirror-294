import re
import datetime

from simhash import Simhash
from langchain_huggingface import HuggingFaceEmbeddings

from aicacia.Document import Document, DocumentSection, MediaType
from aicacia.SimpleFileDocumentExporter import FileDocumentExporter
from aicacia.PreprocessingModel import PreprocessingModel


class Preprocess(PreprocessingModel):
    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )

    def preprocess_batch(self, docs: list[Document]):
        sections = [section for doc in docs for section in doc.sections]
        text_sections = [section for section in sections if section.media_type == MediaType.TEXT]
        embeddings = self.model.embed_documents([section.content for section in text_sections])

        for i, section in enumerate(text_sections):
            section.embedding = embeddings[i]

        for doc in docs:
            if isinstance(doc.raw_content, str):
                doc.content_hash = self.make_simhash(doc.raw_content)

    def make_simhash(self, s):
        return Simhash(self.make_features(s)).value

    @staticmethod
    def make_features(s):
        width = 3
        s = s.lower()
        s = re.sub(r'\W+', '', s)
        return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


if __name__ == '__main__':
    with FileDocumentExporter("test.db", batch_size=32, preprocessing_model=Preprocess()) as exporter:
        exporter.insert([
            Document(
                title="Title 1",
                sections=[
                    DocumentSection("Hello", MediaType.TEXT, 0, metadata={"semantic_position": "Abstract"}),
                    DocumentSection(b"Image", MediaType.IMAGE_JPEG, 100)
                ],
                raw_content="Hello!!!"
            ),
            Document(
                title="Title 2",
                sections=[],
                revision_date=datetime.datetime.now(),
                doi="7890"
            )
        ])
