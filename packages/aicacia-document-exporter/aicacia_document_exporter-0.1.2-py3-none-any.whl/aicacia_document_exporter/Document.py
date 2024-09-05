from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from enum import Enum

import tzlocal


def get_current_time():
    return datetime.now(tzlocal.get_localzone())


class MediaType(Enum):
    TEXT = "text/plain"
    CSV = "text/csv"
    IMAGE_JPEG = "image/jpeg"


@dataclass
class DocumentSection:
    content: str | bytes
    media_type: MediaType | str
    token_offset_position: int
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: list[float] | None = None


@dataclass
class Document:
    title: str
    sections: list[DocumentSection]
    raw_content: str | bytes | None = None
    id: str | None = None
    authors: list[str] = field(default_factory=list)
    doi: str | None = None
    content_hash: int | None = None
    corpus_name: str | None = None
    source_link: str | None = None
    location: str | None = None
    sourced_date: datetime | None = None
    revision_date: datetime | None = None
    provided_tags: list[str] = field(default_factory=list)
    generated_tags: list[str] | None = None
    references: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
