from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
from typing import List

import pandas as pd


@dataclass
class ChunkRecord:
    chunk: str
    source_path: str
    page: int | None = None


class BaseParser(ABC):
    def __init__(self, save_csv_path: str, chunk_size: int= 800, overlap_size: int = 100):
        self.save_csv_path = save_csv_path
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size

    def chunk_text(self, text: str) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.overlap_size
        return chunks

    @abstractmethod
    def parse(self, file_path: str) -> List[ChunkRecord]:
        pass

    def save_to_csv(self, records: List[ChunkRecord]):
        if not records:
            print("No records to save.")
            return
        if os.path.exists(self.save_csv_path):
            df = pd.read_csv(self.save_csv_path)
        else:
            os.makedirs(os.path.dirname(self.save_csv_path), exist_ok=True)
            df = pd.DataFrame(columns=["chunk", "source_path", "page"])
        df_new = pd.DataFrame([record.__dict__ for record in records])
        df_combined = pd.concat([df, df_new], ignore_index=True)
        df_combined.to_csv(self.save_csv_path, index=False)
    
    def __call__(self, file_path: str):
        records = self.parse(file_path)
        self.save_to_csv(records)
        return records
