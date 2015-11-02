BEGIN;

SET client_encoding = 'LATIN1';

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	un text,
	pw text,
	superuser boolean DEFAULT FALSE
	);

INSERT INTO users (un, pw, superuser) VALUES ('root', 'root', TRUE);

COMMIT;

ANALYZE users;