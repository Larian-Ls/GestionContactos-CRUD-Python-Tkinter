DROP DATABASE IF EXISTS contacts;

CREATE DATABASE IF NOT EXISTS contacts;

USE contacts;

CREATE TABLE users (
	name VARCHAR(50),
    tel INT
);

INSERT INTO users VALUES ("Example", 123);

SELECT * FROM users;