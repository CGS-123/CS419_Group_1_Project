BEGIN;

SET client_encoding = 'LATIN1';

CREATE TABLE test_import (
	id SERIAL PRIMARY KEY,
	test text,
	superuser boolean DEFAULT FALSE
	);

INSERT INTO test_import (test, superuser) VALUES ('root', TRUE);

COMMIT;

ANALYZE test_import;