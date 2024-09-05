from typing import Optional
from pydantic import BaseModel


class Result(BaseModel):
    doc_id: str
    page_num: int
    score: float
    base64: Optional[str] = None

    def dict(self):
        return {
            "doc_id": self.doc_id,
            "page_num": self.page_num,
            "score": self.score,
            "base64": self.base64,
        }

    def __getitem__(self, key):
        return getattr(self, key)
