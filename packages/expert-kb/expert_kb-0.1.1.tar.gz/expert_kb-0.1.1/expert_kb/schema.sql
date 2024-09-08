CREATE TABLE IF NOT EXISTS embedded_fragment (
  fragment_id  TEXT  NOT NULL  PRIMARY KEY,
  embedding_id  INTEGER  NOT NULL,
  text  TEXT  NOT NULL,
  metadata_json  TEXT
);
CREATE INDEX embedded_fragment_embedding_id ON embedded_fragment (embedding_id);
