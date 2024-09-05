import json
from pathlib import Path
import struct
from typing import NamedTuple

from expert_kb.sqlite_db import SQLiteDB


class Fragment(NamedTuple):
    fragment_id: str
    text: str
    metadata: dict | None = None
    pass


def serialize(vector: list[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)


class KnowledgeBase:
    def __init__(
        self,
        *,
        path: str,
        embedding_size: int,
    ):
        self.embedding_size = embedding_size
        self.db = SQLiteDB(
            Path(path),
            vector_length=self.embedding_size,
        )
        self.max_embedding_id = self._get_max_embedding_id()
        return

    def _get_max_embedding_id(self) -> int:
        max_row_id = self.db.query(
            """
        select max(rowid) rowid from embedding
        """
        )[0]["rowid"]
        if not max_row_id:
            return 0
        return max_row_id

    def add_fragments(
        self,
        fragments: list[Fragment],
        embeddings: list[list[float]],
    ) -> list[int]:
        assert len(fragments) == len(embeddings)
        return [
            self.add_fragment(
                embedding=embedding,
                **fragment._asdict(),
            )
            for fragment, embedding in zip(fragments, embeddings)
        ]

    def add_fragment(
        self,
        *,
        fragment_id: str,
        text: str,
        embedding: list[float],
        metadata: dict | None = None,
    ) -> int:
        metadata = metadata or {}
        next_embedding_id = self.max_embedding_id + 1
        with self.db.cursor() as cur:
            cur.execute(
                """
            INSERT INTO embedding(
              rowid, embedding
            )
            VALUES (
              :embedding_id, :embedding
            )
            """,
                {
                    "embedding_id": next_embedding_id,
                    "embedding": serialize(embedding),
                },
            )
            cur.execute(
                f"""
            INSERT INTO embedded_fragment(
              fragment_id,
              embedding_id,
              text,
              metadata_json
            ) VALUES (
              :fragment_id,
              :embedding_id,
              :text,
              :metadata_json
            )
            """,
                {
                    "fragment_id": fragment_id,
                    "text": text,
                    "embedding_id": next_embedding_id,
                    "metadata_json": json.dumps(metadata),
                },
            )
            self.max_embedding_id = next_embedding_id
            return next_embedding_id
        pass

    def search(self, embedding: list[float], *, k: int = 5) -> list[Fragment]:
        rows = self.db.query(
            """
        SELECT ef.fragment_id,
               distance,
               ef.text,
               ef.metadata_json
          FROM embedding e
               JOIN embedded_fragment ef ON ef.embedding_id = e.rowid
         WHERE embedding MATCH :embedding
           AND k = :k
         ORDER BY distance
        """,
            {
                "embedding": serialize(embedding),
                "k": k,
            },
        )
        return [
            Fragment(
                fragment_id=row["fragment_id"],
                text=row["text"],
                metadata=json.loads(row["metadata_json"] or "{}"),
            )
            for row in rows
        ]

    pass
