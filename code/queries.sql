BEGIN;

SET client_encoding = 'LATIN1';

CREATE TABLE queries_history (
	id SERIAL PRIMARY KEY,
	query text NOT NULL
	);

CREATE TABLE queries_saved (
	id SERIAL PRIMARY KEY,
	query text NOT NULL
	);

INSERT INTO queries_saved (query) VALUES ('SELECT datname FROM pg_database');

COMMIT;

ANALYZE queries_history;
ANALYZE queries_saved;
