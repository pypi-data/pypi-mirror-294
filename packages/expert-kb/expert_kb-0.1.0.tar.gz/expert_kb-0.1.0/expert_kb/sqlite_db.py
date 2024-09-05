import contextlib
import os
from pathlib import Path
import sqlite3
from string import Template

import sqlite_vec               # type: ignore


EMBEDDING_TABLE_TEMPLATE = Template(
    """
create virtual table embedding using vec0(
  embedding float[${VECTOR_LENGTH}]
)
"""
)

SCHEMA_PATH = Path(os.path.dirname(__file__)) / "./schema.sql"


class SQLiteDB:
    def __init__(self, db_path: Path, *, vector_length: int):
        is_fresh = not db_path.exists()
        self.db_path = db_path
        self.dbcon = sqlite3.connect(db_path)

        self.dbcon.enable_load_extension(True)
        sqlite_vec.load(self.dbcon)
        self.dbcon.enable_load_extension(False)

        self.dbcon.row_factory = sqlite3.Row

        if is_fresh:
            with self.cursor() as cur:
                with open(SCHEMA_PATH, "r") as f:
                    cur.executescript(f.read())
                    pass

                cur.executescript(
                    EMBEDDING_TABLE_TEMPLATE.substitute(
                        {
                            "VECTOR_LENGTH": vector_length,
                        }
                    )
                )
                pass
            pass
        return

    @contextlib.contextmanager
    def cursor(self, autocommit=True):
        cursor = self.dbcon.cursor()
        try:
            yield cursor
            if autocommit:
                self.dbcon.commit()
        finally:
            cursor.close()
        return

    def query(self, *args, **kwargs) -> list[sqlite3.Row]:
        with self.cursor() as cur:
            cur.execute(*args, **kwargs)
            return cur.fetchall()
        pass

    pass
